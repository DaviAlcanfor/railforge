import uuid
import docker
from loguru import logger

from app.schemas.project import ProjectConfig
from app.config.settings import settings
from app.frameworks.registry import get_framework
from app.frameworks.base import BaseFramework


class GeneratorService:
    def __init__(self, config: ProjectConfig):
        self.client = docker.from_env(timeout=settings.DOCKER_TIMEOUT)  # connects to the host Docker socket via /var/run/docker.sock
        self.config = config
        self.framework: BaseFramework = get_framework(config.framework)


    def _build_framework_commands(self) -> list[str]:
        """
        Returns:
            List[str]: ordered list of CLI commands to run inside the container
        """
        cmds = self.framework.commands()
        commands = []

        commands.append(cmds.install)
        commands.append(cmds.create_project.format(project_name=self.config.project_name))

        for model in self.config.models:
            fields = " ".join([f"{field.name}:{field.type}" for field in model.fields])

            commands.append(cmds.generate_model.format(
                model_name=model.name,
                fields=fields
            ))

        if cmds.migrate:
            commands.append(cmds.migrate)

        return commands

    def _build_container_command(self, tar_filename: str) -> str:
        """
        Builds the full bash command:
        1. enters the work directory
        2. runs framework commands
        3. compresses the project into the shared volume
        """
        framework_commands = " && ".join(self._build_framework_commands())

        compress_cmd = settings.RAILS_TAR_CMD.format(
            filename=tar_filename,
            project_name=self.config.project_name
        )

        return f'bash -c "cd {self.framework.WORK_DIR} && {framework_commands} && {compress_cmd}"'


    def generate(self):
        """
        Spins up a temporary container, runs the framework commands,
        tars the output into a shared volume, and returns the raw bytes.

        Returns:
            bytes: raw tar.gz archive of the generated project
        """
        try:
            TAR_FILENAME = f"{self.config.project_name}.tar.gz"

            logger.info(f"Starting generation for project: {self.config.project_name} using {self.framework.NAME}")

            container = self.client.containers.run(
                image=self.framework.DOCKER_IMAGE,
                command=self._build_container_command(TAR_FILENAME),
                name=f"railforge-{self.config.project_name}-{uuid.uuid4().hex[:8]}",
                detach=True,
                remove=False,
                volumes={
                    settings.VOLUME_NAME: {
                        "bind": "/output",
                        "mode": "rw"
                    }
                }
            )

            container.wait()
            logger.info(f"Container finished for project: {self.config.project_name}")
            container.remove()

            output = self.client.containers.run(
                image=settings.ALPINE_IMAGE,
                command=settings.ALPINE_READ_CMD.format(filename=TAR_FILENAME),
                volumes={
                    settings.VOLUME_NAME: {
                        "bind": "/output",
                        "mode": "ro"
                    }
                },
                remove=True
            )

            logger.info(f"Container removed, returning archive for: {self.config.project_name}")
            return output

        except docker.errors.DockerException as e:
            logger.error(f"Docker error during generation: {str(e)}")
            raise RuntimeError(f"Docker error: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error during generation: {str(e)}")
            raise RuntimeError(f"Generation failed: {str(e)}")