import sys
import argparse
from . import enums


# validations
class ValidateNetworks(argparse.Action):
    def __call__(self, parser, args, networks, option_string=None):
        result = []
        for item in networks:
            for network in item.split(" "):
                # try to convert text to chain
                try:
                    net = enums.text_to_chain(network)
                    result.append(net)
                except Exception as e:
                    pass
                # try to convert int to chain
                try:
                    net = enums.int_to_chain(network)
                    result.append(net)
                except Exception as e:
                    pass

        # modify if not empty
        if result:
            setattr(args, self.dest, result)


class ValidateProtocols(argparse.Action):
    def __call__(self, parser, args, protocols, option_string=None):
        valid_subjects = [x.database_name for x in enums.Protocol]

        # modify only if not empty
        if result := [
            protocol
            for item in protocols
            for protocol in item.split(" ")
            if protocol in valid_subjects
        ]:
            setattr(args, self.dest, result)


class ValidateAddresses(argparse.Action):
    def __call__(self, parser, args, addresses, option_string=None):
        # modify only if not empty
        if result := [
            address.lower()
            for item in addresses
            for address in item.split(" ")
            if address[:2] == "0x" and len(address) == 42
        ]:
            setattr(args, self.dest, result)


def parse_commandLine_args(args):
    # main parsers
    par_main = argparse.ArgumentParser(
        prog="gamma_api.py", description=" Gamma api cml tools ", epilog=""
    )

    # exclusive group
    exGroup = par_main.add_mutually_exclusive_group()

    # commands file
    par_cmdfile = exGroup.add_argument(
        "--commands_file",
        type=str,
        help=" specify a formatted commands json file to be executed",
    )

    # manual commands
    par_operations = exGroup.add_argument(
        "--operation",
        choices=[
            "kpi_dashboard",
        ],
        help="choose operation to run",
    )

    # debug
    par_main.add_argument(
        "--debug",
        action="store_true",
        help=" debug mode",
    )

    # datetimes
    par_main.add_argument(
        "--ini_timestamp",
        type=int,
        help="specify an initial timestamp: format integer ",
    )
    par_main.add_argument(
        "--end_timestamp",
        type=int,
        help="specify an ending timestamp: format integer ",
    )
    par_main.add_argument(
        "--period_seconds",
        type=int,
        help="specify the number of seconds each period should have: format integer ",
    )
    par_main.add_argument(
        "--save_to_folder",
        type=str,
        help="specify the folder where to save data to:  format string",
    )

    # par_main.add_argument(
    #     "--ini_block",
    #     type=int,
    #     help="specify an initial block",
    # )
    # par_main.add_argument(
    #     "--end_block",
    #     type=int,
    #     help="specify an ending block ",
    # )

    par_main.add_argument(
        "--addresses",
        action=ValidateAddresses,
        nargs="+",
        help="specify a list of addresses to be processed. Enclose within ' ' separator being an empty space ",
    )

    par_main.add_argument(
        "--networks",
        action=ValidateNetworks,
        nargs="+",
        # type=str,
        help=" specify a list of networks to be processed. Enclose within ' ' separator being an empty space ",
    )
    par_main.add_argument(
        "--protocols",
        action=ValidateProtocols,
        nargs="+",
        # type=str,
        help=" specify a list of protocols to be processed. Enclose within ' ' separator being an empty space ",
    )

    # print helpwhen no command is passed
    return par_main.parse_args(args=args if args else ["--help"])
