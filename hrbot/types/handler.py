from typing import Optional, Iterable, Union, Any
from . import hr

Message = Optional[str | Iterable[str]]
User = Optional[hr.User | Iterable[hr.User]]
CaseIgnoreDefaultValue = False
Reaction = Optional[hr.Reaction | Iterable[hr.Reaction]]
Tip = Optional[Iterable[hr.CurrencyItem | hr.Item]]
Destination = Optional[hr.Position | hr.AnchorPosition | Iterable[hr.Position | hr.AnchorPosition]]
