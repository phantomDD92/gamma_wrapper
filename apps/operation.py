import logging
import apps.kpi_dashboard
import config


def main(option: str):

    networks = config.cfg.CML_PARAMETERS.networks
    protocols = config.cfg.CML_PARAMETERS.protocols
    ini_timestamp = config.cfg.CML_PARAMETERS.ini_timestamp
    end_timestamp = config.cfg.CML_PARAMETERS.end_timestamp
    period_seconds = config.cfg.CML_PARAMETERS.period_seconds
    addresses = config.cfg.CML_PARAMETERS.addresses
    save_to_folder = config.cfg.CML_PARAMETERS.save_to_folder

    if not networks:
        logging.getLogger(__name__).error("Networks not specified.")
        return

    if option == "kpi_dashboard":

        for network in networks:
            if protocols:
                raise NotImplementedError(
                    "Protocols not implemented yet for 'kpi_dashboard' operation."
                )
            apps.kpi_dashboard.create_kpi_dashboard_csv_file(
                chain=config.enums.text_to_chain(network),
                hypervisor_address_list=addresses,
                ini_timestamp=ini_timestamp,
                end_timestamp=end_timestamp,
                period_seconds=period_seconds,
                save_to_folder=save_to_folder,
            )

    else:
        logging.getLogger(__name__).error(f"Option {option} is not valid.")
