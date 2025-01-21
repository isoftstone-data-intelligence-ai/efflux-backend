from pydantic import BaseModel, Field
from typing import Dict, Optional, List
import json
from core.common.logger import get_logger


logger = get_logger(__name__)
config_path = "./server_config.json"


class StdioServerParameters(BaseModel):
    name: Optional[str] = None
    command: str
    args: list[str] = Field(default_factory=list)
    env: Optional[Dict[str, str]] = None


async def load_config_from_file(server_name: str) -> StdioServerParameters:
    """ Load the server configuration from a JSON file. """
    try:
        # debug
        logger.debug(f"Loading config from {config_path}")

        # Read the configuration file
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        # Retrieve the server configuration
        server_config = config.get("mcpServers", {}).get(server_name)
        if not server_config:
            error_msg = f"Server '{server_name}' not found in configuration file."
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Construct the server parameters
        result = StdioServerParameters(
            command=server_config["command"],
            args=server_config.get("args", []),
            env=server_config.get("env"),
        )

        # debug
        logger.debug(f"Loaded config from file: command='{result.command}', args={result.args}, env={result.env}")

        # return result
        return result

    except FileNotFoundError:
        # error
        error_msg = f"Configuration file not found: {config_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    except json.JSONDecodeError as e:
        # json error
        error_msg = f"Invalid JSON in configuration file: {e.msg}"
        logger.error(error_msg)
        raise json.JSONDecodeError(error_msg, e.doc, e.pos)
    except ValueError as e:
        # error
        logger.error(str(e))
        raise


async def load_all_config() -> List[StdioServerParameters]:
    """ Load all the server configuration from a JSON file. """
    try:
        # debug
        logger.debug(f"Loading config from {config_path}")

        # Read the configuration file
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        # Retrieve the server configuration
        server_configs = config.get("mcpServers", {})
        result = []
        for server_name, server_config in server_configs.items():
            result.append(
                StdioServerParameters(
                    name=server_name,
                    command=server_config["command"],
                    args=server_config.get("args", []),
                    env=server_config.get("env"),
                )
            )
        return result
    except FileNotFoundError:
        # error
        error_msg = f"Configuration file not found: {config_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    except json.JSONDecodeError as e:
        # json error
        error_msg = f"Invalid JSON in configuration file: {e.msg}"
        logger.error(error_msg)
        raise json.JSONDecodeError(error_msg, e.doc, e.pos)
    except ValueError as e:
        # error
        logger.error(str(e))
        raise


async def add_config(server: StdioServerParameters) -> StdioServerParameters:
    """ add a server configuration to a JSON file. """
    try:
        # debug
        logger.debug(f"Adding config to {config_path}")

        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        server_param = {"command":server.command, "args":server.args}
        config["mcpServers"][server.server_name] = server_param
        config = json.dumps(config, indent=2, ensure_ascii=False)

        with open(config_path, "w") as config_file:
            config_file.write(config)
        return server

    except FileNotFoundError:
        # error
        error_msg = f"Configuration file not found: {config_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    except json.JSONDecodeError as e:
        # json error
        error_msg = f"Invalid JSON in configuration file: {e.msg}"
        logger.error(error_msg)
        raise json.JSONDecodeError(error_msg, e.doc, e.pos)
    except ValueError as e:
        # error
        logger.error(str(e))
        raise


async def edit_config(server: StdioServerParameters) -> Optional[StdioServerParameters]:
    """ edit a server configuration to a JSON file. """
    try:
        # debug
        logger.debug(f"Updating config to {config_path}")

        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        if server.server_name not in config["mcpServers"].keys():
            return None

        if "command" in config["mcpServers"][server.server_name].keys():
            config["mcpServers"][server.server_name]["command"] = server.command
        if "args" in config["mcpServers"][server.server_name].keys():
            config["mcpServers"][server.server_name]["args"] = server.args
        if "env" in config["mcpServers"][server.server_name].keys():
            config["mcpServers"][server.server_name]["env"] = server.env

        config = json.dumps(config, indent=2, ensure_ascii=False)
        with open(config_path, "w") as config_file:
            config_file.write(config)

        return server

    except FileNotFoundError:
        # error
        error_msg = f"Configuration file not found: {config_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    except json.JSONDecodeError as e:
        # json error
        error_msg = f"Invalid JSON in configuration file: {e.msg}"
        logger.error(error_msg)
        raise json.JSONDecodeError(error_msg, e.doc, e.pos)
    except ValueError as e:
        # error
        logger.error(str(e))
        raise


async def delete_config(server_name: str) -> Optional[str]:
    """ delete a server configuration in a JSON file. """
    try:
        # debug
        logger.debug(f"Deleting a config in {config_path}")

        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        removed_config = config["mcpServers"].pop(server_name, None)
        if not removed_config:
            return None

        config = json.dumps(config, indent=2, ensure_ascii=False)
        with open(config_path, "w") as config_file:
            config_file.write(config)

        return server_name

    except FileNotFoundError:
        # error
        error_msg = f"Configuration file not found: {config_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    except json.JSONDecodeError as e:
        # json error
        error_msg = f"Invalid JSON in configuration file: {e.msg}"
        logger.error(error_msg)
        raise json.JSONDecodeError(error_msg, e.doc, e.pos)
    except ValueError as e:
        # error
        logger.error(str(e))
        raise

