# -*- encoding: utf-8 -*-

"""
A Set of Exceptions/Warnings for the Developer to Handle
"""

class SignatureError(Exception):
    def __init__(self, psignature : str, csignature : str) -> None:
        self.psignature = psignature
        self.csignature = csignature

        super().__init__(
            f"Signature Mismatch: {self.psignature} != {self.csignature}"
        )
