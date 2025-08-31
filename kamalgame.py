import pygame
import random
import math
import time
import os
import json

# تهيئة pygame
pygame.init()
pygame.mixer.init()

# إعدادات الشاشة
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("لعبة سباق الفورمولا المحترفة")

# الألوان
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 20, 60)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# إنشاء مجلد assets إذا لم يكن موجوداً
if not os.path.exists('assets'):
    os.makedirs('assets')

# تحميل الخطوط
try:
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 36)
    font_tiny = pygame.font.Font(None, 24)
except:
    font_large = pygame.font.SysFont('arial', 72)
    font_medium = pygame.font.SysFont('arial', 48)
    font_small = pygame.font.SysFont('arial', 36)
    font_tiny = pygame.font.SysFont('arial', 24)

# دوال المساعدة لرسم النص
def draw_text(text, font, color, x, y, align="center"):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "center":
        text_rect.center = (x, y)
    elif align == "topleft":
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# إنشاء صور برمجياً إذا لم تكن الملفات موجودة
def create_car_image(color, size=(60, 100)):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    # هيكل السيارة
    pygame.draw.rect(surf, color, (5, 0, size[0]-10, size[1]-20))
    pygame.draw.rect(surf, BLACK, (5, 0, size[0]-10, size[1]-20), 2)
    # مقدمة السيارة
    pygame.draw.rect(surf, color, (0, size[1]-20, size[0], 20))
    pygame.draw.rect(surf, BLACK, (0, size[1]-20, size[0], 20), 2)
    # العجلات
    pygame.draw.circle(surf, BLACK, (15, size[1]-10), 8)
    pygame.draw.circle(surf, BLACK, (size[0]-15, size[1]-10), 8)
    pygame.draw.circle(surf, LIGHT_GRAY, (15, size[1]-10), 5)
    pygame.draw.circle(surf, LIGHT_GRAY, (size[0]-15, size[1]-10), 5)
    # الزجاج الأمامي
    pygame.draw.rect(surf, (150, 150, 250, 128), (15, 10, size[0]-30, 15))
    return surf

def create_obstacle_image(type, size=(50, 50)):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    if type == "cone":
        pygame.draw.polygon(surf, ORANGE, [(25, 0), (5, 50), (45, 50)])
        pygame.draw.polygon(surf, WHITE, [(25, 0), (15, 40), (35, 40)])
    elif type == "barrier":
        pygame.draw.rect(surf, RED, (0, 0, 50, 50))
        pygame.draw.rect(surf, WHITE, (0, 0, 50, 10))
        pygame.draw.rect(surf, WHITE, (0, 40, 50, 10))
    else:  # oil
        pygame.draw.circle(surf, BLACK, (25, 25), 25)
        pygame.draw.circle(surf, DARK_GRAY, (25, 25), 20)
        for _ in range(8):
            angle = random.random() * math.pi * 2
            radius = random.randint(5, 15)
            x = 25 + int(radius * math.cos(angle))
            y = 25 + int(radius * math.sin(angle))
            pygame.draw.circle(surf, LIGHT_GRAY, (x, y), 3)
    return surf

def create_track_texture():
    texture = pygame.Surface((800, 600))
    texture.fill(GREEN)  # العشب
    
    # الطريق
    road_width = 600
    pygame.draw.rect(texture, GRAY, (100, 0, road_width, 600))
    
    # خطوط الطريق
    for i in range(0, 600, 50):
        pygame.draw.rect(texture, WHITE, (395, i, 10, 30))
    
    # حواف الطريق
    pygame.draw.rect(texture, WHITE, (100, 0, 10, 600))
    pygame.draw.rect(texture, WHITE, (690, 0, 10, 600))
    
    return texture

def create_grass_texture():
    texture = pygame.Surface((100, 100))
    texture.fill(GREEN)
    # إضافة بعض التفاصيل العشوائية للعشب
    for _ in range(50):
        x = random.randint(0, 99)
        y = random.randint(0, 99)
        color = (0, random.randint(100, 200), 0)
        pygame.draw.circle(texture, color, (x, y), random.randint(1, 3))
    return texture

# تحميل أو إنشاء الصور
def load_or_create_image(filename, create_func, *args):
    try:
        if os.path.exists(f'assets/{filename}'):
            return pygame.image.load(f'assets/{filename}').convert_alpha()
        else:
            image = create_func(*args)
            pygame.image.save(image, f'assets/{filename}')
            return image
    except:
        return create_func(*args)

car_img = load_or_create_image('car.png', create_car_image, RED)
opponent_imgs = [
    load_or_create_image('opponent1.png', create_car_image, BLUE),
    load_or_create_image('opponent2.png', create_car_image, GREEN),
    load_or_create_image('opponent3.png', create_car_image, YELLOW),
    load_or_create_image('opponent4.png', create_car_image, PURPLE)
]

obstacle_imgs = {
    "cone": load_or_create_image('cone.png', create_obstacle_image, "cone"),
    "barrier": load_or_create_image('barrier.png', create_obstacle_image, "barrier"),
    "oil": load_or_create_image('oil.png', create_obstacle_image, "oil")
}

track_texture = load_or_create_image('track.png', create_track_texture)
grass_texture = load_or_create_image('grass.jpg', create_grass_texture)

# إنشاء أصوات برمجياً
def create_engine_sound():
    samples = bytearray()
    for i in range(44100):  # 1 second of audio
        sample = int(127 + 100 * math.sin(2 * math.pi * 300 * i / 44100) * 
                    math.sin(2 * math.pi * 50 * i / 44100))
        samples.append(sample)
    return pygame.mixer.Sound(buffer=bytes(samples))

def create_crash_sound():
    samples = bytearray()
    for i in range(22050):  # 0.5 seconds of audio
        sample = int(127 + 120 * math.sin(2 * math.pi * 200 * i / 22050) *
                    math.exp(-i / 22050))
        samples.append(sample)
    return pygame.mixer.Sound(buffer=bytes(samples))

def create_skid_sound():
    samples = bytearray()
    for i in range(44100):  # 1 second of audio
        sample = int(127 + 80 * math.sin(2 * math.pi * 100 * i / 44100) *
                    (0.5 + 0.5 * math.sin(2 * math.pi * 10 * i / 44100)))
        samples.append(sample)
    return pygame.mixer.Sound(buffer=bytes(samples))

# تحميل أو إنشاء الأصوات
try:
    engine_sound = create_engine_sound()
    crash_sound = create_crash_sound()
    skid_sound = create_skid_sound()
except:
    # أصوات بديلة في حالة الخطأ
    engine_sound = pygame.mixer.Sound(buffer=bytes([127] * 44100))
    crash_sound = pygame.mixer.Sound(buffer=bytes([127] * 22050))
    skid_sound = pygame.mixer.Sound(buffer=bytes([127] * 44100))

# إعدادات الصعوبة
DIFFICULTY_SETTINGS = {
    "easy": {
        "player_speed": 12,
        "opponent_speed": 10,
        "obstacle_frequency": 0.008,
        "damage_multiplier": 0.5,
        "reward_multiplier": 1.5
    },
    "medium": {
        "player_speed": 15,
        "opponent_speed": 12,
        "obstacle_frequency": 0.012,
        "damage_multiplier": 1.0,
        "reward_multiplier": 1.0
    },
    "hard": {
        "player_speed": 18,
        "opponent_speed": 15,
        "obstacle_frequency": 0.018,
        "damage_multiplier": 1.5,
        "reward_multiplier": 0.8
    },
    "expert": {
        "player_speed": 20,
        "opponent_speed": 18,
        "obstacle_frequency": 0.025,
        "damage_multiplier": 2.0,
        "reward_multiplier": 0.6
    }
}

# تحميل الإعدادات
def load_settings():
    default_settings = {
        "difficulty": "medium",
        "sound_volume": 0.7,
        "music_volume": 0.5,
        "controls": {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT},
        "graphics_quality": "medium"
    }
    
    try:
        if os.path.exists('settings.json'):
            with open('settings.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    
    return default_settings

def save_settings(settings):
    try:
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    except:
        pass

settings = load_settings()

# كلاس السيارة
class Car:
    def __init__(self, x, y, img, is_player=False):
        self.x = x
        self.y = y
        self.img = img
        self.width = img.get_width()
        self.height = img.get_height()
        self.speed = 0
        
        diff_settings = DIFFICULTY_SETTINGS[settings["difficulty"]]
        self.max_speed = diff_settings["player_speed"] if is_player else diff_settings["opponent_speed"]
        self.acceleration = 0.2 if is_player else 0.15
        self.deceleration = 0.1
        self.handling = 5 if is_player else 4
        self.damage_multiplier = diff_settings["damage_multiplier"]
        
        self.is_player = is_player
        self.laps = 0
        self.checkpoint_passed = False
        self.crashed = False
        self.crash_time = 0
        self.particles = []
        self.skid_marks = []
        self.skidding = False
    
    def accelerate(self):
        self.speed = min(self.speed + self.acceleration, self.max_speed)
        if self.is_player and self.speed > 5:
            engine_sound.set_volume(min(0.6 * (self.speed / self.max_speed), 0.6) * settings["sound_volume"])
            if not pygame.mixer.get_busy():
                engine_sound.play(-1)
    
    def brake(self):
        self.speed = max(self.speed - self.deceleration * 2, 0)
        if self.speed > 5:
            self.apply_skid()
    
    def coast(self):
        self.speed = max(self.speed - self.deceleration, 0)
        if self.speed < 2:
            engine_sound.stop()
    
    def turn(self, direction):
        if self.speed > 0:
            self.x += direction * self.handling * (self.speed / self.max_speed)
            self.x = max(SCREEN_WIDTH//2 - 300 + self.width//2, 
                        min(self.x, SCREEN_WIDTH//2 + 300 - self.width//2))
            if abs(direction) > 0.5 and self.speed > 8:
                self.apply_skid()
    
    def update(self):
        if self.crashed:
            current_time = pygame.time.get_ticks()
            if current_time - self.crash_time > 2000:
                self.crashed = False
                self.speed = self.max_speed / 2
            return
        
        self.y -= self.speed
        if self.y < -self.height:
            self.y = SCREEN_HEIGHT
            if self.is_player and self.checkpoint_passed:
                self.laps += 1
                self.checkpoint_passed = False
        
        self.update_skid_marks()
        self.update_particles()
    
    def apply_skid(self):
        if self.speed > 5 and not self.skidding:
            self.skidding = True
            skid_sound.set_volume(0.7 * settings["sound_volume"])
            skid_sound.play()
            
            self.skid_marks.append({
                'x': self.x + self.width//2,
                'y': self.y + self.height,
                'width': 8 + int(self.speed / 3),
                'life': 80 + int(self.speed * 2)
            })
        elif self.speed <= 5:
            self.skidding = False
    
    def update_skid_marks(self):
        for skid in self.skid_marks[:]:
            skid['life'] -= 1
            if skid['life'] <= 0:
                self.skid_marks.remove(skid)
    
    def update_particles(self):
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def crash(self):
        if not self.crashed:
            self.crashed = True
            self.crash_time = pygame.time.get_ticks()
            crash_sound.set_volume(0.8 * settings["sound_volume"])
            crash_sound.play()
            
            for _ in range(20):
                self.particles.append({
                    'x': self.x + self.width//2,
                    'y': self.y + self.height//2,
                    'dx': random.uniform(-3, 3),
                    'dy': random.uniform(-3, 3),
                    'radius': random.randint(2, 6),
                    'color': random.choice([RED, ORANGE, YELLOW, BLACK]),
                    'life': random.randint(20, 40)
                })
    
    def draw(self, surface):
        if self.crashed:
            angle = random.randint(-30, 30)
            rotated_img = pygame.transform.rotate(self.img, angle)
            rect = rotated_img.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
            surface.blit(rotated_img, rect.topleft)
            
            for particle in self.particles:
                alpha = min(255, particle['life'] * 6)
                color = list(particle['color']) + [alpha]
                pygame.draw.circle(surface, color, (int(particle['x']), int(particle['y'])), particle['radius'])
        else:
            surface.blit(self.img, (self.x, self.y))
    
    def draw_skid_marks(self, surface):
        for skid in self.skid_marks:
            alpha = min(255, skid['life'] * 3)
            skid_surf = pygame.Surface((skid['width'], 15), pygame.SRCALPHA)
            skid_surf.fill((200, 200, 200, alpha))
            surface.blit(skid_surf, (skid['x'] - skid['width']//2, skid['y']))
    
    def get_rect(self):
        return pygame.Rect(self.x + 10, self.y + 5, self.width - 20, self.height - 10)

# كلاس العقبات
class Obstacle:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.img = obstacle_imgs[type]
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.effect_applied = False
    
    def update(self, speed):
        self.y -= speed
        return self.y < -self.height
    
    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x + 5, self.y + 5, self.width - 10, self.height - 10)
    
    def apply_effect(self, car):
        if not self.effect_applied:
            self.effect_applied = True
            if self.type == "oil":
                car.speed = min(car.speed * 1.3, car.max_speed * 1.3)
                return "oil"
            else:
                car.crash()
                return "crash"
        return None

# دوال الرسم للواجهات
def draw_speedometer():
    center_x = SCREEN_WIDTH - 100
    center_y = SCREEN_HEIGHT - 100
    radius = 80
    
    pygame.draw.circle(screen, DARK_GRAY, (center_x, center_y), radius)
    pygame.draw.circle(screen, WHITE, (center_x, center_y), radius, 3)
    
    for i in range(0, 11):
        angle = math.radians(225 + i * 27)
        start_x = center_x + (radius - 10) * math.cos(angle)
        start_y = center_y + (radius - 10) * math.sin(angle)
        end_x = center_x + radius * math.cos(angle)
        end_y = center_y + radius * math.sin(angle)
        pygame.draw.line(screen, WHITE, (start_x, start_y), (end_x, end_y), 2)
        
        if i % 2 == 0:
            num_x = center_x + (radius - 30) * math.cos(angle)
            num_y = center_y + (radius - 30) * math.sin(angle)
            draw_text(str(i * 20), font_tiny, WHITE, num_x, num_y)
    
    speed_angle = 225 + (player_car.speed / player_car.max_speed) * 270
    needle_x = center_x + (radius - 15) * math.cos(math.radians(speed_angle))
    needle_y = center_y + (radius - 15) * math.sin(math.radians(speed_angle))
    pygame.draw.line(screen, RED, (center_x, center_y), (needle_x, needle_y), 3)
    pygame.draw.circle(screen, RED, (center_x, center_y), 5)
    
    draw_text(f"{int(player_car.speed * 10)} km/h", font_small, WHITE, center_x, center_y + 100)

def draw_hud():
    pygame.draw.rect(screen, (0, 0, 0, 128), (10, 10, 300, 120), border_radius=10)
    pygame.draw.rect(screen, LIGHT_GRAY, (10, 10, 300, 120), 2, border_radius=10)
    
    draw_text(f"السرعة: {int(player_car.speed * 10)} km/h", font_small, WHITE, 20, 25, "topleft")
    draw_text(f"الدور: {player_car.laps}/3", font_small, WHITE, 20, 60, "topleft")
    draw_text(f"النقاط: {score}", font_small, WHITE, 20, 95, "topleft")
    draw_text(f"المستوى: {level}", font_small, WHITE, 20, 130, "topleft")
    
    draw_speedometer()

def draw_menu():
    screen.blit(pygame.transform.scale(grass_texture, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
    
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    draw_text("سباق الفورمولا المحترفة", font_large, RED, SCREEN_WIDTH//2, 150)
    
    menu_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, 250, 400, 350)
    pygame.draw.rect(screen, BLACK, menu_rect, border_radius=20)
    pygame.draw.rect(screen, LIGHT_GRAY, menu_rect, 3, border_radius=20)
    
    options = ["ابدأ اللعبة", "مستوى الصعوبة", "إعدادات الصوت", "التحكم", "المساعدة", "اخرج"]
    for i, text in enumerate(options):
        y_pos = 280 + i * 50
        color = YELLOW if i == selected_menu_item else WHITE
        draw_text(text, font_medium, color, SCREEN_WIDTH//2, y_pos)
    
    diff_names = {"easy": "سهل", "medium": "متوسط", "hard": "صعب", "expert": "خبير"}
    draw_text(f"الصعوبة: {diff_names[settings['difficulty']]}", font_small, LIGHT_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT - 100)
    draw_text("استخدم الأسهم للتحكم: ▲ ▼ ◄ ►", font_small, LIGHT_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50)

def draw_difficulty_menu():
    screen.fill(DARK_GRAY)
    draw_text("اختر مستوى الصعوبة", font_large, RED, SCREEN_WIDTH//2, 100)
    
    difficulties = ["easy", "medium", "hard", "expert"]
    diff_names = {"easy": "سهل", "medium": "متوسط", "hard": "صعب", "expert": "خبير"}
    
    for i, diff in enumerate(difficulties):
        y_pos = 200 + i * 80
        color = GREEN if settings["difficulty"] == diff else WHITE
        
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH//2 - 200, y_pos - 25, 400, 60), border_radius=15)
        pygame.draw.rect(screen, color, (SCREEN_WIDTH//2 - 200, y_pos - 25, 400, 60), 3, border_radius=15)
        
        draw_text(diff_names[diff], font_medium, color, SCREEN_WIDTH//2, y_pos)
        
        diff_set = DIFFICULTY_SETTINGS[diff]
        info_text = f"السرعة: {diff_set['player_speed']} - العقبات: {int(diff_set['obstacle_frequency']*1000)}%"
        draw_text(info_text, font_small, LIGHT_GRAY, SCREEN_WIDTH//2, y_pos + 30)
    
    draw_text("اضغط على ESC للعودة", font_small, LIGHT_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50)

def draw_audio_settings():
    screen.fill(DARK_GRAY)
    draw_text("إعدادات الصوت", font_large, RED, SCREEN_WIDTH//2, 100)
    
    # صوت التأثيرات
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH//2 - 150, 200, 300, 30))
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH//2 - 150, 200, int(300 * settings["sound_volume"]), 30))
    draw_text(f"صوت التأثيرات: {int(settings['sound_volume'] * 100)}%", font_medium, WHITE, SCREEN_WIDTH//2, 180)
    
    # اختبار الصوت
    if pygame.draw.rect(screen, ORANGE, (SCREEN_WIDTH//2 - 75, 250, 150, 40), border_radius=10):
        draw_text("اختبار الصوت", font_medium, BLACK, SCREEN_WIDTH//2, 270)
    
    draw_text("اضغط على ESC للحفظ", font_small, LIGHT_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50)

def draw_control_settings():
    screen.fill(DARK_GRAY)
    draw_text("إعدادات التحكم", font_large, RED, SCREEN_WIDTH//2, 100)
    
    controls_info = [
        ("▲", "التسريع"),
        ("▼", "التبطيء"),
        ("◄", "اليسار"),
        ("►", "اليمين")
    ]
    
    for i, (key, action) in enumerate(controls_info):
        y_pos = 200 + i * 60
        draw_text(action, font_medium, WHITE, SCREEN_WIDTH//2 - 100, y_pos)
        draw_text(key, font_medium, YELLOW, SCREEN_WIDTH//2 + 100, y_pos)
    
    draw_text("اضغط على ESC للعودة", font_small, LIGHT_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50)

def draw_help_menu():
    screen.fill(DARK_GRAY)
    draw_text("تعليمات اللعبة", font_large, RED, SCREEN_WIDTH//2, 80)
    
    instructions = [
        "• استخدم أسهم الاتجاه للتحكم في السيارة",
        "• ▲ للتسريع، ▼ للتبطيء، ◄ ► للتوجيه",
        "• تجنب العقبات والحواجز",
        "• اجمع النقاط بإكمال اللفات",
        "• انتبه لبقع الزيت التي تزيد سرعتك",
        "• استخدم المكابح في المنعطفات الحادة"
    ]
    
    for i, text in enumerate(instructions):
        draw_text(text, font_small, WHITE, SCREEN_WIDTH//2, 150 + i * 40)
    
    draw_text("اضغط على ESC للعودة", font_small, LIGHT_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50)

def draw_pause_menu():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    draw_text("لعبة متوقفة", font_large, WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)
    draw_text("اضغط على P للمواصلة", font_medium, LIGHT_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
    draw_text("اضغط على ESC للخروج", font_small, LIGHT_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120)

def draw_game_over():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    draw_text("انتهت اللعبة!", font_large, RED, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100)
    draw_text(f"النقاط النهائية: {score}", font_medium, WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    draw_text(f"عدد اللفات: {player_car.laps}", font_medium, WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
    draw_text("اضغط على ESC للعودة للقائمة", font_small, LIGHT_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 150)

# إعدادات اللعبة الرئيسية
clock = pygame.time.Clock()
FPS = 60

# حالات اللعبة
game_states = ["menu", "playing", "paused", "game_over", "difficulty", "audio", "controls", "help"]
game_state = "menu"
selected_menu_item = 0

# متغيرات اللعبة
player_car = None
opponents = []
obstacles = []
track_y = 0
score = 0
level = 1
max_level = 5
obstacle_frequency = 0.01
checkpoint = pygame.Rect(SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT - 100, 600, 20)

# تهيئة اللعبة
def init_game():
    global player_car, opponents, obstacles, track_y, score, level, obstacle_frequency
    
    player_car = Car(SCREEN_WIDTH//2 - 30, SCREEN_HEIGHT - 200, car_img, True)
    
    opponents = []
    for i in range(4):
        lane = random.randint(0, 3)
        x = SCREEN_WIDTH//2 - 250 + lane * 150
        y = -random.randint(100, 1000)
        opponents.append(Car(x, y, random.choice(opponent_imgs)))
    
    obstacles = []
    track_y = 0
    score = 0
    level = 1
    
    diff_settings = DIFFICULTY_SETTINGS[settings["difficulty"]]
    obstacle_frequency = diff_settings["obstacle_frequency"]
    
    engine_sound.set_volume(0.6 * settings["sound_volume"])

# الحلقة الرئيسية للعبة
running = True
init_game()

while running:
    # التعامل مع الأحداث
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state in ["difficulty", "audio", "controls", "help"]:
                    game_state = "menu"
                    save_settings(settings)
                elif game_state == "playing":
                    game_state = "paused"
                elif game_state == "paused":
                    game_state = "menu"
                elif game_state == "game_over":
                    game_state = "menu"
            
            elif event.key == pygame.K_RETURN:
                if game_state == "menu":
                    if selected_menu_item == 0:  # ابدأ اللعبة
                        game_state = "playing"
                        init_game()
                    elif selected_menu_item == 1:  # مستوى الصعوبة
                        game_state = "difficulty"
                    elif selected_menu_item == 2:  # إعدادات الصوت
                        game_state = "audio"
                    elif selected_menu_item == 3:  # التحكم
                        game_state = "controls"
                    elif selected_menu_item == 4:  # المساعدة
                        game_state = "help"
                    elif selected_menu_item == 5:  # اخرج
                        running = False
            
            elif event.key == pygame.K_p and game_state == "playing":
                game_state = "paused"
            elif event.key == pygame.K_p and game_state == "paused":
                game_state = "playing"
            
            elif event.key == pygame.K_UP and game_state == "menu":
                selected_menu_item = (selected_menu_item - 1) % 6
            elif event.key == pygame.K_DOWN and game_state == "menu":
                selected_menu_item = (selected_menu_item + 1) % 6
    
    # التحديث والرسم بناء على حالة اللعبة
    if game_state == "playing":
        # التحكم في السيارة
        keys = pygame.key.get_pressed()
        if keys[settings["controls"]["up"]]:
            player_car.accelerate()
        elif keys[settings["controls"]["down"]]:
            player_car.brake()
        else:
            player_car.coast()
        
        if keys[settings["controls"]["left"]]:
            player_car.turn(-1)
        if keys[settings["controls"]["right"]]:
            player_car.turn(1)
        
        # تحديث المسار
        track_y = (track_y + player_car.speed) % track_texture.get_height()
        
        # تحديث السيارة
        player_car.update()
        
        # تحديث الخصوم
        for opponent in opponents:
            opponent.update()
            if opponent.y > SCREEN_HEIGHT:
                opponent.y = -opponent.height
                opponent.x = SCREEN_WIDTH//2 - 250 + random.randint(0, 3) * 150
                opponent.speed = random.uniform(5, opponent.max_speed)
            
            if player_car.get_rect().colliderect(opponent.get_rect()) and not player_car.crashed:
                player_car.crash()
                score = max(0, score - 50)
        
        # تحديث العقبات
        for obstacle in obstacles[:]:
            if obstacle.update(player_car.speed):
                obstacles.remove(obstacle)
                score += 10
            elif player_car.get_rect().colliderect(obstacle.get_rect()) and not player_car.crashed:
                effect = obstacle.apply_effect(player_car)
                if effect == "crash":
                    score = max(0, score - 30)
                obstacles.remove(obstacle)
        
        # إضافة عقبات جديدة
        if random.random() < obstacle_frequency:
            obstacle_type = random.choice(list(obstacle_imgs.keys()))
            lane = random.randint(0, 3)
            x = SCREEN_WIDTH//2 - 250 + lane * 150 + random.randint(-30, 30)
            obstacles.append(Obstacle(x, SCREEN_HEIGHT + 100, obstacle_type))
        
        # التحقق من نقطة检查
        if checkpoint.colliderect(player_car.get_rect()):
            player_car.checkpoint_passed = True
        
        # زيادة النقاط
        score += int(player_car.speed / 10)
        
        # زيادة مستوى الصعوبة
        if score > level * 1000 and level < max_level:
            level += 1
            obstacle_frequency += 0.005
            for opponent in opponents:
                opponent.max_speed += 1
                opponent.acceleration += 0.05
        
        # التحقق من انتهاء اللعبة
        if player_car.laps >= 3:
            game_state = "game_over"
        
        # الرسم
        screen.blit(pygame.transform.scale(track_texture, (SCREEN_WIDTH, SCREEN_HEIGHT)), 
                   (0, track_y - track_texture.get_height()))
        screen.blit(pygame.transform.scale(track_texture, (SCREEN_WIDTH, SCREEN_HEIGHT)), 
                   (0, track_y))
        
        # رسم نقطة检查
        pygame.draw.rect(screen, GREEN if player_car.checkpoint_passed else RED, checkpoint)
        
        # رسم العقبات
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # رسم الخصوم
        for opponent in opponents:
            opponent.draw(screen)
            opponent.draw_skid_marks(screen)
        
        # رسم سيارة اللاعب
        player_car.draw(screen)
        player_car.draw_skid_marks(screen)
        
        # رسم واجهة المستخدم
        draw_hud()
    
    elif game_state == "menu":
        draw_menu()
    
    elif game_state == "paused":
        draw_pause_menu()
    
    elif game_state == "game_over":
        draw_game_over()
    
    elif game_state == "difficulty":
        draw_difficulty_menu()
    
    elif game_state == "audio":
        draw_audio_settings()
    
    elif game_state == "controls":
        draw_control_settings()
    
    elif game_state == "help":
        draw_help_menu()
    
    # تحديث الشاشة
    pygame.display.flip()
    clock.tick(FPS)

# حفظ الإعدادات والخروج
save_settings(settings)
pygame.quit()
