"""
Data models for Scan Pipeline output validation.
"""

from typing import List, Dict, Optional, Tuple
from pydantic import BaseModel, Field
from enum import Enum


class CaptureTier(str, Enum):
    PHOTOS = "photos"
    VIDEO = "video"
    LIDAR = "lidar"


class OpeningType(str, Enum):
    DOOR = "door"
    WINDOW = "window"
    PASSAGEWAY = "passageway"


class SurfaceType(str, Enum):
    WALL = "wall"
    CEILING = "ceiling"
    FLOOR = "floor"


class DamageSeverity(str, Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ConfidenceInterval(BaseModel):
    lower: float
    upper: float
    margin_pct: Optional[float] = None


class PropertySummary(BaseModel):
    total_floor_area_sq_m: float
    total_rooms: int
    confidence_interval: ConfidenceInterval


class WallModel(BaseModel):
    wall_id: str
    length_m: float
    length_ci: Optional[ConfidenceInterval] = None
    start_point: List[float]
    end_point: List[float]
    orientation_deg: Optional[float] = 0.0


class OpeningModel(BaseModel):
    opening_id: str
    wall_id: str
    type: OpeningType
    width_m: float
    width_ci: Optional[ConfidenceInterval] = None
    height_m: float
    offset_from_wall_start_m: Optional[float] = 0.0


class RoomDimensions(BaseModel):
    ceiling_height_m: float
    ceiling_height_ci: Optional[ConfidenceInterval] = None
    floor_area_sq_m: float
    floor_area_ci: Optional[ConfidenceInterval] = None
    perimeter_m: float


class RoomModel(BaseModel):
    room_id: str
    name: str
    dimensions: RoomDimensions
    walls: List[WallModel]
    openings: List[OpeningModel]


class AdjacencyEdge(BaseModel):
    room_a: str
    room_b: str
    connector_type: str
    shared_opening_id: str


class RoomPlacement(BaseModel):
    translation: List[float]
    rotation_deg: float
    polygon: List[List[float]]


class StitchedPlanModel(BaseModel):
    adjacency_graph: List[AdjacencyEdge]
    room_placements: Dict[str, RoomPlacement]
    drift_metric_m: float


class DamageRegionModel(BaseModel):
    damage_id: str
    room_id: str
    surface_id: str
    surface_type: SurfaceType
    damage_class: str
    metric_extent_sq_m: float
    extent_ci: Optional[ConfidenceInterval] = None
    severity: DamageSeverity
    location_polygon: Optional[List[List[float]]] = None


class ConcealedDamageFlagModel(BaseModel):
    flag_id: str
    rule_id: str
    rule_name: str
    surface_id: str
    room_id: Optional[str] = None
    risk_level: RiskLevel
    description: str
    action_required: str


class ScopeLineItemModel(BaseModel):
    line_item_id: str
    item_code: str
    category: str
    description: str
    surface_id: str
    quantity: float
    unit: str
    unit_cost_usd: Optional[float] = None
    estimated_cost_usd: float


class CaptureOutputModel(BaseModel):
    capture_id: str
    tier: CaptureTier
    device_model: str
    timestamp: str
    processing_time_sec: float
    drift_corrected: bool
    property_summary: PropertySummary
    rooms: Dict[str, RoomModel]
    multi_room_stitched_plan: StitchedPlanModel
    damage_regions: List[DamageRegionModel]
    concealed_damage_flags: List[ConcealedDamageFlagModel]
    scope_line_items: List[ScopeLineItemModel]
