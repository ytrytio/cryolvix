from dataclasses import dataclass, field
from random import randint
from typing_extensions import Optional

@dataclass(kw_only=True)
class GPUModel:
    model: str
    prefix: str
    series: int
    level: int
    company: str
    price: int = 0
    multiplier: float
    suffix: str = ""
    
    def calculate_price(self, min_price: int = 10000, max_price: int = 500000) -> int:
        def score(s, l):
            return 150.0 * s + 10.0 * l + 2.0 * (l ** 2)

        score_min = score(1, 0)
        score_max = score(9, 9)

        current_score = score(self.series, self.level)
        t = (current_score - score_min) / (score_max - score_min)
        t = max(0.0, min(1.0, t))

        price = min_price + t * (max_price - min_price)
        return int(round(price / 100.0) * 100)
        
    @property
    def product_id(self) -> tuple:
        gpuid = ""
        gpuid += self.company.lower() + "_"
        gpuid += self.prefix.lower() + "_"
        gpuid += str(self.series) + "_"
        gpuid += str(self.level) + "_"
        gpuid += self.suffix.lower()
        return ("gpu", gpuid)
        
    @staticmethod
    def from_id(id: str) -> Optional["GPUModel"]:
        try:
            items = id.split("_")
            company = items[0]
            prefix = items[1].upper()
            series = int(items[2])
            level = int(items[3])
            suffix = items[4].upper()

            if company == "gnd":
                return GNDGPU(prefix=prefix, series=series, level=level, suffix=suffix)
            if company == "novideo":
                return NoVideoGPU(prefix=prefix, series=series, level=level, suffix=suffix)

            return None
        except:
            return None


@dataclass
class NoVideoGPU(GPUModel):
    company: str = "NoVideo"
    prefix: str = "NTX"

    series: int = 0
    level: int = 0
    model: str = field(init=False)
    multiplier: float = field(init=False)

    def __post_init__(self):
        self.prefix = "HTX" if self.series < 2 else "NTX"
        self.model = f"{self.company} {self.prefix} {self.series}0{self.level}0{self.suffix}".strip()

        def score(s, l):
            return 220.0 * s + 8.0 * l + 3.0 * (l ** 2)

        score_min = score(1, 5)
        score_max = score(5, 9)

        current_score = score(self.series, self.level)
        t = (current_score - score_min) / (score_max - score_min)
        t = max(0.0, min(1.0, t))

        raw_mul = 2.0 + t * 6.0
        self.multiplier = round(raw_mul * 4) / 4
        self.multiplier = max(2.0, min(8.0, self.multiplier))

        self.price = self.calculate_price(15000, 600000)

    def calculate_price(self, min_price: int = 15000, max_price: int = 600000) -> int:
        def score(s, l):
            return 220.0 * s + 8.0 * l + 3.0 * (l ** 2)

        score_min = score(1, 5)
        score_max = score(5, 9)

        current_score = score(self.series, self.level)
        t = (current_score - score_min) / (score_max - score_min)
        t = max(0.0, min(1.0, t))

        price = min_price + t * (max_price - min_price)
        return int(round(price / 100.0) * 100)

    @staticmethod
    def generate() -> "NoVideoGPU":
        return NoVideoGPU(
            series=randint(1, 5),
            level=randint(5, 9),
            suffix=""
        )


@dataclass
class GNDGPU(GPUModel):
    company: str = "GND"
    prefix: str = "TX"

    series: int = 0
    level: int = 0
    model: str = field(init=False)
    multiplier: float = field(init=False)

    def __post_init__(self):
        self.model = f"{self.company} {self.prefix} {self.series}{self.level}0{'0' if self.series >= 6 else ''}{self.suffix}".strip()

        def score(s, l):
            return 180.0 * s + 7.0 * l + 2.5 * (l ** 2)

        score_min = score(5, 5)
        score_max = score(9, 9)

        current_score = score(self.series, self.level)
        t = (current_score - score_min) / (score_max - score_min)
        t = max(0.0, min(1.0, t))

        raw_mul = 2.0 + t * 6.0
        self.multiplier = round(raw_mul * 4) / 4
        self.multiplier = max(2.0, min(8.0, self.multiplier))

        self.price = self.calculate_price(10000, 480000)

    def calculate_price(self, min_price: int = 10000, max_price: int = 480000) -> int:
        def score(s, l):
            return 180.0 * s + 7.0 * l + 2.5 * (l ** 2)

        score_min = score(5, 5)
        score_max = score(9, 9)

        current_score = score(self.series, self.level)
        t = (current_score - score_min) / (score_max - score_min)
        t = max(0.0, min(1.0, t))

        price = min_price + t * (max_price - min_price)
        return int(round(price / 100.0) * 100)

    @staticmethod
    def generate() -> "GNDGPU":
        return GNDGPU(
            series=randint(5, 9),
            level=randint(5, 9),
            suffix=""
        )


  
"""    
@dataclass
class SteudGPU(GPUModel):
    company: str = "Steud"
    prefix: str = "Bogen"
    
    series: int = 0
    level: int = 0
    model: str = field(init=False)
    multiplier: float = field(init=False)

    def __post_init__(self):
        self.model = f"{self.company} {self.prefix} X{self.series}{self.level}0"
        self.multiplier = (self.series//3) + (self.level//2) + len(self.suffix) if len(self.suffix) <= 3 else 3
        self.price = self.calculate_price()

TX580 = GNDGPU(series=5, level=8, price=15000)
TX9060 = GNDGPU(series=9, level=6, price=45000)
TX7090 = GNDGPU(series=7, level=9, price=80000)

BOGEN120 = SteudGPU(series=1, level=2, price=8000)
BOGEN450 = SteudGPU(series=4, level=5, price=25000)
BOGEN790 = SteudGPU(series=7, level=9, price=70000)

NTX650 = NoVideoGPU(series=6, level=5, price=12000)
NTX3040 = NoVideoGPU(series=3, level=4, price=35000)
NTX9020 = NoVideoGPU(series=9, level=2, price=95000)

GPUS = {
    v.model.lower().replace(" ", "_"): v 
    for k, v in locals().items() 
    if isinstance(v, GPUModel)
}

"""
