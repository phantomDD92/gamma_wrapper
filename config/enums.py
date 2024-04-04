from enum import Enum


class Chain(str, Enum):
    #      ( value , id , database_name, fantasy_name )
    ARBITRUM = ("arbitrum", 42161, "arbitrum", "Arbitrum")
    CELO = ("celo", 42220, "celo", "Celo")
    ETHEREUM = ("ethereum", 1, "ethereum", "Ethereum")
    OPTIMISM = ("optimism", 10, "optimism", "Optimism")
    POLYGON = ("polygon", 137, "polygon", "Polygon")
    BSC = ("bsc", 56, "binance", "Binance Chain")
    POLYGON_ZKEVM = (
        "polygon_zkevm",
        1101,
        "polygon_zkevm",
        "Polygon zkEVM",
    )
    AVALANCHE = ("avalanche", 43114, "avalanche", "Avalanche")
    FANTOM = ("fantom", 250, "fantom", "Fantom")
    MOONBEAM = ("moonbeam", 1284, "moonbeam", "Moonbeam")

    MANTLE = ("mantle", 5000, "mantle", "Mantle")

    BASE = ("base", 8453, "base", "Base")

    LINEA = ("linea", 59144, "linea", "Linea")

    ROLLUX = ("rollux", 570, "rollux", "Rollux")

    OPBNB = ("opbnb", 204, "opbnb", "OpBNB")

    KAVA = ("kava", 2222, "kava", "Kava")

    MANTA = ("manta", 169, "manta", "Manta")
    METIS = ("metis", 1088, "metis", "Metis")

    GNOSIS = ("gnosis", 100, "gnosis", "Gnosis")

    ASTAR_ZKEVM = ("astar_zkevm", 3776, "astar_zkevm", "Astar zkEVM")

    IMMUTABLE_ZKEVM = ("immutable_zkevm", 13371, "immutable_zkevm", "Immutable zkEVM")

    BLAST = ("blast", 81457, "blast", "Blast")

    # extra properties
    id: int
    database_name: str
    fantasy_name: str

    def __new__(
        self,
        value: str,
        id: int,
        database_name: str | None = None,
        fantasy_name: str | None = None,
    ):
        """_summary_

        Args:
            value (str): _description_
            id (int): _description_
            database_name (str | None, optional): . Defaults to value.
            fantasy_name (str | None, optional): . Defaults to value.

        Returns:
            _type_: _description_
        """
        obj = str.__new__(self, value)
        obj._value_ = value
        obj.id = id
        # optional properties
        obj.database_name = database_name or value.lower()
        obj.fantasy_name = fantasy_name or value.lower()
        return obj


class Protocol(str, Enum):
    #  ( value , database_name, fantasy_name )
    GAMMA = ("gamma", "gamma", "Gamma Strategies")

    ALGEBRAv3 = ("algebrav3", "algebrav3", "AlgebraV3")
    UNISWAPv3 = ("uniswapv3", "uniswapv3", "Uniswap")

    PANCAKESWAP = ("pancakeswap", "pancakeswap", "PancakeSwap")  # univ3 mod

    BEAMSWAP = ("beamswap", "beamswap", "Beamswap")  # univ3 mod
    CAMELOT = ("camelot", "camelot", "Camelot")  # algebra mods
    QUICKSWAP = ("quickswap", "quickswap", "QuickSwap")  # algebra and univ3
    QUICKSWAP_UNISWAP = (
        "quickswap_uniswap",
        "quickswap_uniswap",
        "QuickSwap",
    )  # only for polygon-zkevm now ( have both algebra and univ3)
    ZYBERSWAP = ("zyberswap", "zyberswap", "Zyberswap")
    THENA = ("thena", "thena", "Thena")
    GLACIER = ("glacier", "glacier", "Glacier")
    SPIRITSWAP = ("spiritswap", "spiritswap", "SpiritSwap")
    SUSHI = ("sushi", "sushi", "Sushi")
    RETRO = ("retro", "retro", "Retro")
    STELLASWAP = ("stellaswap", "stellaswap", "StellaSwap")

    RAMSES = ("ramses", "ramses", "Ramses")
    VEZARD = ("vezard", "vezard", "veZard")
    EQUILIBRE = ("equilibre", "equilibre", "Equilibre")

    ASCENT = ("ascent", "ascent", "Ascent")

    SYNTHSWAP = ("synthswap", "synthswap", "SynthSwap")
    LYNEX = ("lynex", "lynex", "Lynex")

    ZERO = ("zero", "zero", "Zero")

    BASEX = ("basex", "basex", "BaseX")

    FUSIONX = ("fusionx", "fusionx", "FusionX")

    PEGASYS = ("pegasys", "pegasys", "Pegasys")

    APERTURE = ("aperture", "aperture", "Aperture")
    HERCULES = ("hercules", "hercules", "Hercules")

    BASESWAP = ("baseswap", "baseswap", "BaseSwap")
    SWAPBASED = ("swapbased", "swapbased", "SwapBased")

    PHARAOH = ("pharaoh", "pharaoh", "Pharaoh")  # ramses avalanche
    CLEOPATRA = ("cleopatra", "cleopatra", "Cleopatra")  # ramses mantle

    KINETIX = ("kinetix", "kinetix", "Kinetix")

    SWAPR = ("swapr", "swapr", "Swapr")  # gnosis
    THICK = ("thick", "thick", "Thick")

    BLASTER = ("blaster", "blaster", "Blaster")

    # extra properties
    database_name: str
    fantasy_name: str

    def __new__(
        self,
        value: str,
        database_name: str | None = None,
        fantasy_name: str | None = None,
    ):
        """

        Args:
            value (_type_): chain name
            id (_type_): chain id

        Returns:
            : Chain
        """
        obj = str.__new__(self, value)
        obj._value_ = value
        # optional properties
        obj.database_name = database_name or value.lower()
        obj.fantasy_name = fantasy_name or value.lower()
        return obj


class Period(str, Enum):
    ##       value  api_url, api_name, subgraph_name, database_name, cron, days
    DAILY = (
        "daily",
        None,
        None,
        None,
        None,
        "*/60 */2 * * *",
        1,
    )  # (At every 60th minute past every 2nd hour. )
    WEEKLY = (
        "weekly",
        None,
        None,
        None,
        None,
        "*/60 */12 * * *",
        7,
    )  # (At every 60th minute past every 12th hour. )
    BIWEEKLY = (
        "biweekly",
        None,
        None,
        None,
        None,
        "0 6 */1 * *",
        14,
    )  # ( At 06:00 on every day-of-month.)
    MONTHLY = (
        "monthly",
        None,
        None,
        None,
        None,
        "0 12 */2 * *",
        30,
    )  # ( At 12:00 on every 2nd day-of-month.)
    # BIMONTHLY = ("bimonthly", None, None, None, None, None, "0 12 */4 * *", 60)
    QUARTERLY = (
        "quarterly",
        None,
        None,
        None,
        None,
        "0 4 */6 * *",
        90,
    )  # ( At 00:00 on every 6th day-of-month.)
    BIANNUAL = (
        "biannual",
        None,
        None,
        None,
        None,
        "0 15 */12 * *",
        180,
    )  # ( At 00:00 on every 12th day-of-month.)
    YEARLY = ("yearly", None, None, None, None, "0 2 */24 * *", 365)

    # extra properties
    api_url: str
    api_name: str
    subgraph_name: str
    database_name: str
    cron: str
    days: int

    def __new__(
        self,
        value: str,
        api_url: str | None = None,
        api_name: str | None = None,
        subgraph_name: str | None = None,
        database_name: str | None = None,
        cron: str | None = None,
        days: int | None = None,
    ):
        """

        Args:
            value (_type_): chain name
            id (_type_): chain id

        Returns:
            : Chain
        """
        obj = str.__new__(self, value)
        obj._value_ = value
        # optional properties
        obj.api_url = api_url or value.lower()
        obj.api_name = api_name or value.lower()
        obj.subgraph_name = subgraph_name or value.lower()
        obj.database_name = database_name or value.lower()
        obj.cron = cron or ""
        obj.days = days or 0
        return obj


# HELPERS
def text_to_chain(text: str) -> Chain:
    """Text to Chain conversion

    Args:
        text (str): what to find

    Returns:
        Chain:
    """
    for chain in Chain:
        if text.lower() in [
            chain.value.lower(),
            chain.database_name.lower(),
            chain.fantasy_name.lower(),
        ]:
            return chain

    if text.lower() == "polygon-zkevm":
        return Chain.POLYGON_ZKEVM
    elif text.lower() == "mainnet":
        return Chain.ETHEREUM
    raise ValueError(f"Chain with text {text} not found")


def int_to_chain(num: int) -> Chain:
    """Chain id to Chain enum conversion

    Args:
        num (int): chain id

    Returns:
        Protocol:
    """
    for ch in Chain:
        if num == ch.id:
            return ch
    raise ValueError(f"Chain id {num} not found")


def text_to_protocol(text: str) -> Protocol:
    """Text to Protocol conversion

    Args:
        text (str): what to find

    Returns:
        Protocol:
    """
    for protocol in Protocol:
        if text.lower() in [
            protocol.value.lower(),
            protocol.database_name.lower(),
            protocol.fantasy_name.lower(),
        ]:
            return protocol
    raise ValueError(f"Protocol with text {text} not found")


def int_to_period(num: int) -> Period:
    """Day numbers to Protocol conversion

    Args:
        num (int): days

    Returns:
        Protocol:
    """
    for per in Period:
        if num == per.days:
            return per
    raise ValueError(f"Period with days {num} not found")
