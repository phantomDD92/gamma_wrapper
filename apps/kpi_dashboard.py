from datetime import datetime, timezone
import logging
import time
import config.enums
import api_wrapper.objects
import utils


def create_kpi_dashboard_csv_file(
    chain: config.enums.Chain,
    hypervisor_address_list: list[str] | None = None,
    ini_timestamp: int | None = None,
    end_timestamp: int | None = None,
    period_seconds: int | None = None,
    save_to_folder: str | None = None,
) -> None:

    # create data
    data = build_kpi_dashboard_data(
        chain=chain,
        hypervisor_address_list=hypervisor_address_list,
        ini_timestamp=ini_timestamp,
        end_timestamp=end_timestamp,
        period_seconds=period_seconds,
    )
    # convert to csv and save to file
    if csv_string := utils.convert.convert_to_csv(data):

        # save to file
        if not utils.file.save_text(
            filename=create_filename(
                chain=chain,
                ini_timestamp=ini_timestamp,
                end_timestamp=end_timestamp,
                period_seconds=period_seconds,
                hypervisor_address_list=hypervisor_address_list,
            ),
            text=csv_string,
            folder_path=save_to_folder,
        ):
            logging.getLogger(__name__).error("Error saving csv file.")

    else:
        logging.getLogger(__name__).error("Error creating csv file.")


def build_kpi_dashboard_data(
    chain: config.enums.Chain,
    hypervisor_address_list: list[str] | None = None,
    ini_timestamp: int | None = None,
    end_timestamp: int | None = None,
    period_seconds: int | None = None,
) -> list[dict]:

    # create helper
    gamma_api_helper = api_wrapper.objects.gamma_api()

    # create a list of ini_timestamp,end_timestamp tuples for each period
    periods = []
    if period_seconds:
        # calculate the periods
        end_timestamp = end_timestamp or int(time.time())
        while end_timestamp > ini_timestamp:
            periods.append((end_timestamp - period_seconds, end_timestamp))
            end_timestamp -= period_seconds
    elif ini_timestamp and end_timestamp:
        periods.append((ini_timestamp, end_timestamp))
    elif ini_timestamp:
        periods.append((ini_timestamp, time.time()))
    elif end_timestamp:
        periods.append((0, end_timestamp))
    else:
        periods.append((0, time.time()))

    result = []
    # reverse the periods
    periods = periods[::-1]

    logging.getLogger(__name__).debug(
        f" Building kpi dashboard data of {len(periods)} periods for {chain.fantasy_name} from {datetime.fromtimestamp(ini_timestamp, tz=timezone.utc) if ini_timestamp else ''} to {datetime.fromtimestamp(end_timestamp, tz=timezone.utc) if end_timestamp else ''}."
    )

    for ini_time, end_time in periods:

        # get the data
        average_tvl = gamma_api_helper.internal_kpi_average_tvl(
            chain=chain,
            hypervisor_addresses=hypervisor_address_list,
            ini_timestamp=ini_time,
            end_timestamp=end_time,
        )
        transactions_summary = gamma_api_helper.internal_kpi_transactions_summary(
            chain=chain,
            hypervisor_addresses=hypervisor_address_list,
            ini_timestamp=ini_time,
            end_timestamp=end_time,
        )
        user_activity = gamma_api_helper.internal_kpi_user_activity(
            chain=chain,
            hypervisor_addresses=hypervisor_address_list,
            ini_timestamp=ini_time,
            end_timestamp=end_time,
        )
        transactions = gamma_api_helper.internal_kpi_transactions(
            chain=chain,
            hypervisor_addresses=hypervisor_address_list,
            ini_timestamp=ini_time,
            end_timestamp=end_time,
        )

        transactions = (
            transactions.get(chain.id, {})
            or transactions.get(str(chain.id), {})
            or {
                "deposits_qtty": 0,
                "withdraws_qtty": 0,
                "zeroBurns_qtty": 0,
                "rebalances_qtty": 0,
                "transfers_qtty": 0,
            }
        )

        # append the data
        result.append(
            {
                "ini_timestamp": average_tvl["ini_timestamp"],
                "end_timestamp": average_tvl["end_timestamp"],
                "average_tvl": average_tvl["average_tvl"],
                "fees": transactions_summary["fees_usd"],
                "gross_fees": transactions_summary["gross_fees_usd"],
                "volume": transactions_summary["volume"],
                "deposits": transactions["deposits_qtty"],
                "withdraws": transactions["withdraws_qtty"],
                "compounds": transactions["zeroBurns_qtty"],
                "rebalances": transactions["rebalances_qtty"],
                "transfers": transactions["transfers_qtty"],
                "users": user_activity["total_users"],
            }
        )

        utils.progress.print_progress_bar(
            current=periods.index((ini_time, end_time)),
            total=len(periods),
            description=f" {chain.fantasy_name}",
        )

    # return the result
    return result


def create_filename(
    chain: config.enums.Chain,
    ini_timestamp: int | None = None,
    end_timestamp: int | None = None,
    period_seconds: int | None = None,
    hypervisor_address_list: list[str] | None = None,
) -> str:
    # create file name
    filename = f"kpi_dashboard_{chain.id}"
    if ini_timestamp:
        filename += f"_{ini_timestamp}"
    if end_timestamp:
        filename += f"_{end_timestamp}"
    if period_seconds:
        filename += f"_{period_seconds}"
    if hypervisor_address_list:
        filename += f"_{len(hypervisor_address_list)}"

    return f"{filename}.csv"
