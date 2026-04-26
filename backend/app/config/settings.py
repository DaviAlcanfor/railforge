from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RUBY_IMAGE: str = "railforge-rails"
    RAILS_INSTALL_CMD: str = "" # no need anymore as i built a image in Dockerfile.rails
    RAILS_MIGRATE_CMD: str = "rails db:migrate"
    ARCHIVE_MEDIA_TYPE: str = "application/x-tar"
    ARCHIVE_CONTENT: str = "attachment; filename={project_name}.tar"
    VOLUME_NAME: str = "railforge_output"
    DOCKER_TIMEOUT: int = 300
    RAILS_TAR_CMD: str = "tar -czf /output/{filename} {project_name}"
    ALPINE_IMAGE: str = "alpine"
    ALPINE_READ_CMD: str = "cat /output/{filename}"
    RAILS_WORK_DIR: str = "/projects"
    VOLUME_BIND_RW: dict = {"bind": "/output", "mode": "rw"}
    VOLUME_BIND_RO: dict = {"bind": "/output", "mode": "ro"}
    

settings = Settings()