from fuzzywuzzy import fuzz, process
import re
from typing import List
from pydantic import BaseModel


class MerchantGroup(BaseModel):
    group_name: str
    merchants: List[str]
    count: int


class SimpleMerchantClassifier:
    def __init__(self):
        pass

    def clean_name(self, name: str) -> str:
        """Clean merchant name"""
        # Remove numbers and special characters
        cleaned = re.sub(r"[0-9]+", "", name)
        cleaned = re.sub(r"[^\w\s]", " ", cleaned)
        cleaned = " ".join(cleaned.split()).strip().lower()
        return cleaned

    def group_merchants(
        self, merchants: List[str], threshold: int = 80
    ) -> List[MerchantGroup]:
        """Group merchants using fuzzy matching"""
        groups = []
        used_merchants = set()

        for merchant in merchants:
            if merchant in used_merchants:
                continue

            # Find similar merchants
            similar_merchants = [merchant]
            used_merchants.add(merchant)

            clean_merchant = self.clean_name(merchant)

            for other_merchant in merchants:
                if other_merchant in used_merchants:
                    continue

                clean_other = self.clean_name(other_merchant)
                similarity = fuzz.ratio(clean_merchant, clean_other)

                if similarity >= threshold:
                    similar_merchants.append(other_merchant)
                    used_merchants.add(other_merchant)

            # Use cleaned name as group name
            group_name = clean_merchant or merchant

            groups.append(
                MerchantGroup(
                    group_name=group_name,
                    merchants=similar_merchants,
                    count=len(similar_merchants),
                )
            )

        return groups


# uv add fuzzywuzzy python-levenshtein
