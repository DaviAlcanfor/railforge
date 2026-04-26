import uuid
import docker
from loguru import logger

from app.schemas.project import ProjectConfig
from app.config.settings import settings



class GeneratorService:
    def __init__(self, config: ProjectConfig):
        self.client = docker.from_env(timeout=settings.DOCKER_TIMEOUT)  # connects to the host Docker socket via /var/run/docker.sock
        self.config = config


    def _build_container_command(self, tar_filename: str) -> str:
        """
        Builds the full bash command:
        1. enters the work directory
        2. runs Rails commands
        3. compresses the project into the shared volume
        """
        rails_commands = " && ".join(self.build_rails_commands())

        compress_cmd = settings.RAILS_TAR_CMD.format(
            filename=tar_filename,
            project_name=self.config.project_name
        )

        cmd = f'bash -c "cd {settings.RAILS_WORK_DIR} && {rails_commands} && {compress_cmd}"'
        return cmd

    def build_rails_commands(self) -> list[str]:
        """
        Returns:
            List[str]: ordered list of Rails CLI commands to run inside the container
        """

        # creates the rails project w/ the --api flag
        commands = [f"rails new {self.config.project_name} --api"]

        for model in self.config.models:
            fields = " ".join([f"{field.name}:{field.type}" for field in model.fields])
            commands.append(f"rails generate model {model.name} {fields}")

        commands.append(settings.RAILS_MIGRATE_CMD)
        return commands

    def generate(self):
        """
        Spins up a temporary Rails container, runs the commands,
        tars the output into a shared volume, and returns the raw bytes.

        Returns:
            bytes: raw tar.gz archive of the generated Rails project
        """
        try:
            tar_filename = f"{self.config.project_name}.tar.gz"

            logger.info(f"Starting generation for project: {self.config.project_name}")

            container = self.client.containers.run(
                image=settings.RUBY_IMAGE,
                command=self._build_container_command(tar_filename),
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
                command=settings.ALPINE_READ_CMD.format(filename=tar_filename),
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