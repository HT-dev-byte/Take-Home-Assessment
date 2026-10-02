"""
Damage Region Extractor, Concealed Damage Rule Engine, and Scope Line Item Estimator.
Identifies surface damage, fires concealed damage rules, and maps scope repair items.
"""

from typing import Dict, List, Any, Tuple

# Rule definitions for concealed damage evaluation
CONCEALED_DAMAGE_RULES = [
    {
        "rule_id": "RULE_WATER_STAIN_PLUMBING",
        "rule_name": "Adjacent Wet-Wall Moisture & Mold Risk",
        "condition": lambda dmg: dmg.get("damage_class") == "water_stain" and dmg.get("surface_type") in ["wall", "ceiling"],
        "risk_level": "high",
        "description": "Water stain on wall or ceiling near plumbing/wet stack indicates sub-surface drywall saturation & mold risk.",
        "action_required": "Infrared thermal moisture scan, moisture meter probe, & sub-surface cavity inspection."
    },
    {
        "rule_id": "RULE_STRUCTURAL_CRACK_LOAD_BEARING",
        "rule_name": "Diagonal Shear Stress & Structural Settlement",
        "condition": lambda dmg: dmg.get("damage_class") == "shear_crack" or (dmg.get("damage_class") == "crack" and dmg.get("metric_extent_sq_m", 0) > 1.0),
        "risk_level": "critical",
        "description": "Diagonal shear crack over 1.0m on perimeter wall suggests foundational settlement or structural movement.",
        "action_required": "Structural engineering assessment & laser leveling verification."
    },
    {
        "rule_id": "RULE_FLOOR_BUCKLING_SUBFLOOR",
        "rule_name": "Subfloor Delamination & Joist Moisture Saturation",
        "condition": lambda dmg: dmg.get("damage_class") == "floor_buckling" or (dmg.get("damage_class") == "water_stain" and dmg.get("surface_type") == "floor"),
        "risk_level": "high",
        "description": "Hardwood or laminate floor buckling indicates trapped subfloor moisture & joist degradation.",
        "action_required": "Remove finished floor section, assess plywood subfloor & timber joist moisture content."
    }
]

# Cost database mapping damage class -> scope line item
REPAIR_CATALOG = {
    "water_stain": {
        "item_code": "DRY-WTR-REPAIR",
        "category": "Drywall & Painting",
        "description": "Cut out wet drywall, apply stain-blocking primer, patch and paint surface",
        "unit": "sq_m",
        "unit_cost_usd": 95.0
    },
    "shear_crack": {
        "item_code": "STR-CRK-STITCH",
        "category": "Structural & Masonry",
        "description": "Epoxy injection crack repair, carbon fiber helical stitch, skim coat finish",
        "unit": "linear_m",
        "unit_cost_usd": 220.0
    },
    "crack": {
        "item_code": "DRY-CRK-REPAIR",
        "category": "Drywall",
        "description": "Mesh tape wall crack, joint compound fill, sand and paint matching finish",
        "unit": "sq_m",
        "unit_cost_usd": 65.0
    },
    "floor_buckling": {
        "item_code": "FLR-WOOD-REPLACE",
        "category": "Flooring",
        "description": "Remove buckled flooring, dry subfloor, replace underlayment and floor planks",
        "unit": "sq_m",
        "unit_cost_usd": 140.0
    }
}


class DamageEngine:
    @staticmethod
    def process_damage_and_scope(raw_damage_regions: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        processed_damage = []
        concealed_flags = []
        scope_items = []

        for idx, dmg in enumerate(raw_damage_regions):
            dmg_id = dmg.get("damage_id", f"dmg_{idx+1}")
            room_id = dmg.get("room_id", "room_1")
            surface_id = dmg.get("surface_id", "w1")
            surface_type = dmg.get("surface_type", "wall")
            dmg_class = dmg.get("damage_class", "water_stain")
            extent = float(dmg.get("metric_extent_sq_m", 1.0))
            severity = dmg.get("severity", "moderate")

            processed_damage.append({
                "damage_id": dmg_id,
                "room_id": room_id,
                "surface_id": surface_id,
                "surface_type": surface_type,
                "damage_class": dmg_class,
                "metric_extent_sq_m": round(extent, 2),
                "extent_ci": {
                    "lower": round(extent * 0.95, 2),
                    "upper": round(extent * 1.05, 2)
                },
                "severity": severity,
                "location_polygon": dmg.get("location_polygon", [[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5]])
            })

            # Check concealed damage rules
            for rule in CONCEALED_DAMAGE_RULES:
                if rule["condition"](dmg):
                    flag_id = f"flag_{len(concealed_flags)+1}"
                    concealed_flags.append({
                        "flag_id": flag_id,
                        "rule_id": rule["rule_id"],
                        "rule_name": rule["rule_name"],
                        "surface_id": surface_id,
                        "room_id": room_id,
                        "risk_level": rule["risk_level"],
                        "description": rule["description"],
                        "action_required": rule["action_required"]
                    })

            # Key scope line item to surface
            catalog_entry = REPAIR_CATALOG.get(dmg_class, REPAIR_CATALOG["water_stain"])
            cost = round(extent * catalog_entry["unit_cost_usd"], 2)
            item_id = f"item_{len(scope_items)+1}"

            scope_items.append({
                "line_item_id": item_id,
                "item_code": catalog_entry["item_code"],
                "category": catalog_entry["category"],
                "description": catalog_entry["description"],
                "surface_id": surface_id,
                "quantity": round(extent, 2),
                "unit": catalog_entry["unit"],
                "unit_cost_usd": catalog_entry["unit_cost_usd"],
                "estimated_cost_usd": cost
            })

        return processed_damage, concealed_flags, scope_items
