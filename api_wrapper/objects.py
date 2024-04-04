from config.enums import Chain, Protocol
import config.cfg as cfg
import utils.net


class gamma_api:
    def __init__(self) -> None:
        self._server = cfg.API_URL

    # BASE CALL
    def _get_response(self, url_middle_part: str, variables: list[tuple]):

        if not url_middle_part.startswith("/"):
            url_middle_part = f"/{url_middle_part}"

        _url = f"{self._server}{url_middle_part}"
        # add variables to url
        if variables:
            _url += "?"
            _first = True
            for key, value in variables:
                if _first:
                    _url += f"{key}={value}"
                    _first = False
                else:
                    _url += f"&{key}={value}"

        try:
            return utils.net.get_response(
                url=_url,
            )
        except Exception as e:
            pass

    # GET TYPE REQUESTS
    def get_json(self, url_middle_part: str, variables: list[tuple]) -> dict:

        try:
            result = self._get_response(
                url_middle_part=url_middle_part,
                variables=variables,
            ).json()
        except Exception as e:
            pass
        return result

    def get_csv(self, url_middle_part: str, variables: list[tuple]) -> list[dict]:

        try:
            result = self._get_response(
                url_middle_part=url_middle_part,
                variables=variables,
            ).text.split("\n")
        except Exception as e:
            pass
        return result

    # ENDPOINTS
    def frontend_analytics_returns_csv(
        self, hypervisor_address: str, chain: Chain, period: str | int
    ) -> list[dict]:

        return self.get_csv(
            url_middle_part="/frontend/analytics/returns/csv",
            variables=[
                ("hypervisor_address", hypervisor_address),
                ("chain", chain.id),
                ("period", period),
            ],
        )

    def internal_reports_kpi_dashboard(
        self,
        chain: Chain,
        protocol: Protocol | None = None,
        hypervisor_addresses: list[str] | None = None,
        ini_timestamp: int | None = None,
        end_timestamp: int | None = None,
        period_seconds: int | None = None,
    ) -> dict:

        # build variables
        variables = [
            ("chain", chain.id),
        ]
        if protocol:
            variables.append(("protocol", protocol.database_name))
        if ini_timestamp:
            variables.append(("ini_timestamp", ini_timestamp))
        if end_timestamp:
            variables.append(("end_timestamp", end_timestamp))
        if period_seconds:
            variables.append(("period_seconds", period_seconds))
        if hypervisor_addresses:
            variables += [
                ("hypervisor_addresses", address) for address in hypervisor_addresses
            ]

        return self.get_json(
            url_middle_part="/internal/reports/kpi_dashboard",
            variables=variables,
        )

    def internal_kpi_average_tvl(
        self,
        chain: Chain,
        protocol: Protocol | None = None,
        hypervisor_addresses: list[str] | None = None,
        ini_timestamp: int | None = None,
        end_timestamp: int | None = None,
    ) -> dict:
        # build variables
        variables = []
        if protocol:
            variables.append(("protocol", protocol.database_name))
        if ini_timestamp:
            variables.append(("ini_timestamp", ini_timestamp))
        if end_timestamp:
            variables.append(("end_timestamp", end_timestamp))
        if hypervisor_addresses:
            variables += [("hypervisors", address) for address in hypervisor_addresses]

        return self.get_json(
            url_middle_part=f"/internal/internal/kpi/{chain.value if chain != Chain.ETHEREUM else 'mainnet'}/average_tvl",
            variables=variables,
        )

    def internal_kpi_transactions(
        self,
        chain: Chain,
        protocol: Protocol | None = None,
        hypervisor_addresses: list[str] | None = None,
        ini_timestamp: int | None = None,
        end_timestamp: int | None = None,
    ) -> dict:
        # build variables
        variables = []
        if protocol:
            variables.append(("protocol", protocol.database_name))
        if ini_timestamp:
            variables.append(("ini_timestamp", ini_timestamp))
        if end_timestamp:
            variables.append(("end_timestamp", end_timestamp))
        if hypervisor_addresses:
            variables += [("hypervisors", address) for address in hypervisor_addresses]

        return self.get_json(
            url_middle_part=f"/internal/internal/kpi/{chain.value if chain != Chain.ETHEREUM else 'mainnet'}/transactions",
            variables=variables,
        )

    def internal_kpi_transactions_summary(
        self,
        chain: Chain,
        protocol: Protocol | None = None,
        hypervisor_addresses: list[str] | None = None,
        ini_timestamp: int | None = None,
        end_timestamp: int | None = None,
    ) -> dict:

        # build variables
        variables = []
        if protocol:
            variables.append(("protocol", protocol.database_name))
        if ini_timestamp:
            variables.append(("ini_timestamp", ini_timestamp))
        if end_timestamp:
            variables.append(("end_timestamp", end_timestamp))
        if hypervisor_addresses:
            variables += [("hypervisors", address) for address in hypervisor_addresses]

        return self.get_json(
            url_middle_part=f"/internal/internal/kpi/{chain.value if chain != Chain.ETHEREUM else 'mainnet'}/transactions_summary",
            variables=variables,
        )

    def internal_kpi_user_activity(
        self,
        chain: Chain,
        hypervisor_addresses: list[str] | None = None,
        ini_timestamp: int | None = None,
        end_timestamp: int | None = None,
    ) -> dict:
        # build variables
        variables = [
            ("chain", chain.value if chain != Chain.ETHEREUM else "mainnet"),
        ]
        if ini_timestamp:
            variables.append(("ini_timestamp", ini_timestamp))
        if end_timestamp:
            variables.append(("end_timestamp", end_timestamp))
        if hypervisor_addresses:
            variables += [("hypervisors", address) for address in hypervisor_addresses]

        return self.get_json(
            url_middle_part="/internal/internal/kpi/user_activity", variables=variables
        )
