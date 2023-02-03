import math
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from PIL import Image

@dataclass_json
@dataclass
class Config:
	"""Class for holding configuration for a single algo run."""
	beta: float
	rho: float
	sigma: float
	dt: float
	iterations: int
	result_size: int

@dataclass
class Point:
	x: float
	y: float
	z: float

@dataclass
class Bounds:
	min: Point
	max: Point

	def expand(self, p: Point):
		if p.x < self.min.x:
			self.min.x = p.x
		if p.y < self.min.y:
			self.min.y = p.y
		if p.z < self.min.z:
			self.min.z = p.z
		if p.x > self.max.x:
			self.max.x = p.x
		if p.y > self.max.y:
			self.max.y = p.y
		if p.z > self.max.z:
			self.max.z = p.z

	def translate(self, p: Point, result_size: int) -> Point:
		relX = (p.x - self.min.x) / (self.max.x - self.min.x)
		relY = (p.y - self.min.y) / (self.max.y - self.min.y)
		relZ = (p.z - self.min.z) / (self.max.z - self.min.z)
		s = float(result_size - 1)
		return Point(
			relX * s,
			relY * s,
			relZ * s,
		)

def next_step(cfg: Config, p: Point) -> Point:
	dxdt = cfg.sigma * (p.y - p.x)
	dydt = p.x*(cfg.rho-p.z) - p.y
	dzdt = p.x*p.y - cfg.beta*p.z
	return Point(
		p.x + dxdt*cfg.dt,
		p.y + dydt*cfg.dt,
		p.z + dzdt*cfg.dt,
	)

def run(cfg: Config) -> Image:
	points = []
	points.append(Point(1, 1, 1))
	bounds = Bounds(Point(1, 1, 1), Point(1, 1, 1))

	for i in range(1, cfg.iterations):
		point = next_step(cfg, points[i-1])
		points.append(point)
		bounds.expand(point)

	for i, point in enumerate(points):
		points[i] = bounds.translate(point, cfg.result_size)

	counts = [[0 for col in range(cfg.result_size)] for row in range(cfg.result_size)]
	max_count = 0
	for point in points:
		x = int(math.floor(point.x))
		y = int(math.floor(point.y))
		counts[x][y] += 1
		if counts[x][y] > max_count:
			max_count = counts[x][y]

	img = Image.new("RGB", (cfg.result_size, cfg.result_size))
	pixels = img.load()
	for i in range(len(counts)):
		for j in range(len(counts[i])):
			count = counts[i][j]
			if count != 0:
				pos = math.sqrt(math.sqrt(float(count) / float(max_count)))
				b = int(pos*200) % 256 + 55
				g = int((1-pos)*200) % 256 + 55
				pixels[i,j] = (0, g, b)
	return img