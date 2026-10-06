"""Base dos modelos Pydantic de ENTRADA: rejeita qualquer campo não declarado (extra='forbid').

Todo body recebido pela API deve herdar de StrictRequest.
"""

from pydantic import BaseModel, ConfigDict


class StrictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
