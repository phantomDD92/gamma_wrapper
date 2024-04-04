import os
import sys
import logging
from datetime import datetime, timezone

import apps
import config.cfg
from config.command_line import parse_commandLine_args
import utils.objects

# set working directory the script's
os.chdir(os.path.dirname(os.path.realpath(__file__)))


def main():
    if config.cfg.CML_PARAMETERS.debug:
        # setup application logging
        logging.basicConfig(filename="debug.log", encoding="utf-8", level=logging.DEBUG)
    else:
        # setup application logging
        logging.basicConfig(filename="info.log", encoding="utf-8", level=logging.INFO)

    # choose the first of the  parsed options
    if config.cfg.CML_PARAMETERS.operation:
        #  --operation
        apps.operation.main(option=config.cfg.CML_PARAMETERS.operation)
    else:
        # nothin todo
        logging.getLogger(__name__).info(" Nothing to do. How u doin? ")


# START ####################################################################################################################
if __name__ == "__main__":
    print(f" Python version: {sys.version}")

    __module_name = " Gamma API cmd line access tool"

    ##### main ######
    logging.getLogger(__name__).info(
        f" Start {__module_name}   ----------------------> "
    )

    # start time log
    _startime = datetime.now(timezone.utc)

    # check if commands file is passed
    if config.cfg.CML_PARAMETERS.commands_file:
        #  --commands_file
        _commands_filename = config.cfg.CML_PARAMETERS.commands_file
        # remove extension if present
        if _commands_filename.endswith(".json"):
            _commands_filename = _commands_filename[:-5]
        # get folder path
        _commands_file_folder = os.path.dirname(config.cfg.CML_PARAMETERS.commands_file)
        if not os.path.exists(_commands_file_folder):
            # use current folder
            _commands_file_folder = os.path.dirname(os.path.realpath(__file__))
        # load file
        commands_file = utils.file.load_json(
            filename=_commands_filename,
            folder_path=_commands_file_folder,
        )
        # save original CML parameters
        original_cml_parameters = config.cfg.CML_PARAMETERS
        # execute commands
        for commands_list in commands_file["commands"]:
            # set new CML parameters
            config.cfg.CML_PARAMETERS = parse_commandLine_args(commands_list)
            # execute
            main()
        # restore original CML parameters
        config.cfg.CML_PARAMETERS = original_cml_parameters
    else:
        # no commands file
        main()

    logging.getLogger(__name__).info(
        f" took {utils.objects.log_time_passed.get_timepassed_string(start_time=_startime)} to complete"
    )
    logging.getLogger(__name__).info(
        f" Exit {__module_name}    <----------------------"
    )
