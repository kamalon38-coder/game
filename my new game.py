from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, Line, Ellipse, Triangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from kivy.storage.jsonstore import JsonStore

import random
import math

# إعدادات اللعبة
class GameConfig:
    def __init__(self):
        self.store = JsonStore('game_settings.json')
        if not self.store.exists('settings'):
            self.store.put('settings', 
                difficulty='medium',
                sound_volume=0.7,
                music_volume=0.5,
                controls_type='tilt',  # tilt أو touch
                graphics_quality='medium'
            )
    
    def get_setting(self, key):
        return self.store.get('settings')[key]
    
    def set_setting(self, key, value):
        settings = self.store.get('settings')
        settings[key] = value
        self.store.put('settings', **settings)

config = GameConfig()

# شاشة البداية
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        title = Label(
            text='سباق الفورمولا',
            font_size=48,
            size_hint=(1, 0.3),
            color=(1, 0.2, 0.2, 1)
        )
        
        btn_play = Button(
            text='بدء اللعبة',
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        btn_play.bind(on_press=self.start_game)
        
        btn_settings = Button(
            text='الإعدادات',
            size_hint=(1, 0.2),
            background_color=(0.2, 0.4, 0.8, 1)
        )
        btn_settings.bind(on_press=self.open_settings)
        
        btn_help = Button(
            text='المساعدة',
            size_hint=(1, 0.2),
            background_color=(0.8, 0.6, 0.2, 1)
        )
        btn_help.bind(on_press=self.open_help)
        
        layout.add_widget(title)
        layout.add_widget(btn_play)
        layout.add_widget(btn_settings)
        layout.add_widget(btn_help)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        self.manager.current = 'game'
    
    def open_settings(self, instance):
        self.manager.current = 'settings'
    
    def open_help(self, instance):
        self.manager.current = 'help'

# شاشة الإعدادات
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(
            text='الإعدادات',
            font_size=36,
            size_hint=(1, 0.1),
            color=(1, 1, 1, 1)
        )
        
        # مستوى الصعوبة
        diff_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        diff_label = Label(text='الصعوبة:', size_hint=(0.4, 1))
        self.diff_btn = Button(text=config.get_setting('difficulty'), size_hint=(0.6, 1))
        self.diff_btn.bind(on_press=self.change_difficulty)
        diff_layout.add_widget(diff_label)
        diff_layout.add_widget(self.diff_btn)
        
        # نوع التحكم
        control_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        control_label = Label(text='نوع التحكم:', size_hint=(0.4, 1))
        self.control_btn = Button(text=config.get_setting('controls_type'), size_hint=(0.6, 1))
        self.control_btn.bind(on_press=self.change_control_type)
        control_layout.add_widget(control_label)
        control_layout.add_widget(self.control_btn)
        
        # جودة الرسومات
        graphics_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        graphics_label = Label(text='جودة الرسومات:', size_hint=(0.4, 1))
        self.graphics_btn = Button(text=config.get_setting('graphics_quality'), size_hint=(0.6, 1))
        self.graphics_btn.bind(on_press=self.change_graphics_quality)
        graphics_layout.add_widget(graphics_label)
        graphics_layout.add_widget(self.graphics_btn)
        
        # صوت المؤثرات
        sound_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1))
        sound_label = Label(text='صوت المؤثرات:')
        self.sound_slider = Slider(min=0, max=1, value=config.get_setting('sound_volume'))
        self.sound_slider.bind(value=self.on_sound_volume)
        sound_layout.add_widget(sound_label)
        sound_layout.add_widget(self.sound_slider)
        
        # صوت الموسيقى
        music_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1))
        music_label = Label(text='صوت الموسيقى:')
        self.music_slider = Slider(min=0, max=1, value=config.get_setting('music_volume'))
        self.music_slider.bind(value=self.on_music_volume)
        music_layout.add_widget(music_label)
        music_layout.add_widget(self.music_slider)
        
        # زر العودة
        back_btn = Button(
            text='العودة',
            size_hint=(1, 0.1),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        back_btn.bind(on_press=self.go_back)
        
        layout.add_widget(title)
        layout.add_widget(diff_layout)
        layout.add_widget(control_layout)
        layout.add_widget(graphics_layout)
        layout.add_widget(sound_layout)
        layout.add_widget(music_layout)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def change_difficulty(self, instance):
        difficulties = ['easy', 'medium', 'hard', 'expert']
        current = config.get_setting('difficulty')
        index = difficulties.index(current)
        new_index = (index + 1) % len(difficulties)
        config.set_setting('difficulty', difficulties[new_index])
        self.diff_btn.text = difficulties[new_index]
    
    def change_control_type(self, instance):
        types = ['tilt', 'touch']
        current = config.get_setting('controls_type')
        index = types.index(current)
        new_index = (index + 1) % len(types)
        config.set_setting('controls_type', types[new_index])
        self.control_btn.text = types[new_index]
    
    def change_graphics_quality(self, instance):
        qualities = ['low', 'medium', 'high']
        current = config.get_setting('graphics_quality')
        index = qualities.index(current)
        new_index = (index + 1) % len(qualities)
        config.set_setting('graphics_quality', qualities[new_index])
        self.graphics_btn.text = qualities[new_index]
    
    def on_sound_volume(self, instance, value):
        config.set_setting('sound_volume', value)
    
    def on_music_volume(self, instance, value):
        config.set_setting('music_volume', value)
    
    def go_back(self, instance):
        self.manager.current = 'start'

# شاشة المساعدة
class HelpScreen(Screen):
    def __init__(self, **kwargs):
        super(HelpScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(
            text='تعليمات اللعبة',
            font_size=36,
            size_hint=(1, 0.1),
            color=(1, 1, 1, 1)
        )
        
        scroll = ScrollView(size_hint=(1, 0.8))
        help_text = """
        • استخدم الميلان أو اللمس للتحكم في السيارة
        • تجنب العقبات والحواجز على الطريق
        • اجمع النقاط بإكمال اللفات حول المضمار
        • انتبه لبقع الزيت التي تزيد سرعتك
        • استخدم المكابح في المنعطفات الحادة
        • حاول إكمال 3 لفات للفوز بالسباق
        
        أنواع العقبات:
        - المخاريط البرتقالية: تجنبها
        - الحواجز الحمراء: تجنبها
        - بقع الزيت السوداء: تزيد سرعتك
        
        تحكم:
        - الميلان: أمِل الجهاز للتحكم
        - اللمس: اضغط على الجانب الأيسر أو الأيمن
        
        يمكنك تغيير نوع التحكم من شاشة الإعدادات.
        """
        
        content = Label(
            text=help_text,
            font_size=20,
            text_size=(Window.width - 40, None),
            size_hint_y=None,
            height=600
        )
        scroll.add_widget(content)
        
        back_btn = Button(
            text='العودة',
            size_hint=(1, 0.1),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        back_btn.bind(on_press=self.go_back)
        
        layout.add_widget(title)
        layout.add_widget(scroll)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'start'

# لعبة السباق الرئيسية
class RacingGame(Screen):
    car_x = NumericProperty(0)
    car_y = NumericProperty(0)
    score = NumericProperty(0)
    laps = NumericProperty(0)
    speed = NumericProperty(0)
    game_over = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(RacingGame, self).__init__(**kwargs)
        
        # إعدادات الصعوبة
        self.difficulty = config.get_setting('difficulty')
        self.difficulty_settings = {
            'easy': {'player_speed': 8, 'opponent_speed': 6, 'obstacle_freq': 0.005},
            'medium': {'player_speed': 10, 'opponent_speed': 8, 'obstacle_freq': 0.008},
            'hard': {'player_speed': 12, 'opponent_speed': 10, 'obstacle_freq': 0.012},
            'expert': {'player_speed': 15, 'opponent_speed': 12, 'obstacle_freq': 0.02}
        }
        
        # متغيرات اللعبة
        self.road_width = Window.width * 0.6
        self.road_left = Window.width * 0.2
        self.car_width = Window.width * 0.1
        self.car_height = self.car_width * 1.6
        self.car_x = Window.width / 2 - self.car_width / 2
        self.car_y = Window.height * 0.2
        self.max_speed = self.difficulty_settings[self.difficulty]['player_speed']
        self.speed = 0
        self.acceleration = 0.2
        self.deceleration = 0.1
        self.handling = 5
        self.score = 0
        self.laps = 0
        self.max_laps = 3
        self.game_over = False
        
        # الخصوم والعقبات
        self.opponents = []
        self.obstacles = []
        self.obstacle_frequency = self.difficulty_settings[self.difficulty]['obstacle_freq']
        
        # التحكم
        self.control_type = config.get_setting('controls_type')
        self.touch_x = 0
        
        # المؤثرات الصوتية
        self.engine_sound = None
        self.crash_sound = None
        self.load_sounds()
        
        # مؤشر السرعة
        self.speedometer = Speedometer()
        self.add_widget(self.speedometer)
        
        # أزرار التحكم باللمس
        if self.control_type == 'touch':
            self.setup_touch_controls()
        
        # بدء تحديث اللعبة
        Clock.schedule_interval(self.update, 1.0/60.0)
        
        # رسم الطريق
        self.draw_road()
    
    def load_sounds(self):
        try:
            self.engine_sound = SoundLoader.load('assets/engine.wav')
            self.crash_sound = SoundLoader.load('assets/crash.wav')
            if self.engine_sound:
                self.engine_sound.loop = True
                self.engine_sound.volume = config.get_setting('sound_volume')
            if self.crash_sound:
                self.crash_sound.volume = config.get_setting('sound_volume')
        except:
            pass
    
    def setup_touch_controls(self):
        # أزرار اللمس على الجانبين
        left_btn = Button(
            size_hint=(0.2, 0.3),
            pos_hint={'x': 0, 'y': 0},
            opacity=0.3,
            background_color=(0, 0, 1, 0.3)
        )
        left_btn.bind(on_press=self.touch_left)
        
        right_btn = Button(
            size_hint=(0.2, 0.3),
            pos_hint={'x': 0.8, 'y': 0},
            opacity=0.3,
            background_color=(1, 0, 0, 0.3)
        )
        right_btn.bind(on_press=self.touch_right)
        
        accel_btn = Button(
            size_hint=(0.6, 0.3),
            pos_hint={'x': 0.2, 'y': 0},
            opacity=0.3,
            background_color=(0, 1, 0, 0.3)
        )
        accel_btn.bind(on_press=self.touch_accelerate)
        
        brake_btn = Button(
            size_hint=(0.6, 0.15),
            pos_hint={'x': 0.2, 'y': 0.15},
            opacity=0.3,
            background_color=(1, 0, 0, 0.3)
        )
        brake_btn.bind(on_press=self.touch_brake)
        
        self.add_widget(left_btn)
        self.add_widget(right_btn)
        self.add_widget(accel_btn)
        self.add_widget(brake_btn)
    
    def draw_road(self):
        with self.canvas:
            # الخلفية (العشب)
            Color(0.2, 0.6, 0.2)
            Rectangle(pos=(0, 0), size=(Window.width, Window.height))
            
            # الطريق
            Color(0.4, 0.4, 0.4)
            Rectangle(pos=(self.road_left, 0), size=(self.road_width, Window.height))
            
            # خطوط الطريق
            Color(1, 1, 1)
            line_height = Window.height / 20
            for i in range(20):
                y_pos = i * line_height * 2 + (self.speed % (line_height * 2))
                Rectangle(
                    pos=(Window.width/2 - 5, y_pos),
                    size=(10, line_height)
                )
            
            # حواف الطريق
            Line(points=[self.road_left, 0, self.road_left, Window.height], width=2)
            Line(points=[self.road_left + self.road_width, 0, 
                         self.road_left + self.road_width, Window.height], width=2)
    
    def on_touch_down(self, touch):
        if self.control_type == 'touch':
            self.touch_x = touch.x
        return super(RacingGame, self).on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if self.control_type == 'touch':
            self.touch_x = touch.x
        return super(RacingGame, self).on_touch_move(touch)
    
    def touch_left(self, instance):
        self.turn(-1)
    
    def touch_right(self, instance):
        self.turn(1)
    
    def touch_accelerate(self, instance):
        self.accelerate()
    
    def touch_brake(self, instance):
        self.brake()
    
    def accelerate(self):
        self.speed = min(self.speed + self.acceleration, self.max_speed)
        if self.engine_sound and not self.engine_sound.state == 'play':
            self.engine_sound.play()
    
    def brake(self):
        self.speed = max(self.speed - self.deceleration * 2, 0)
    
    def coast(self):
        self.speed = max(self.speed - self.deceleration, 0)
        if self.speed < 2 and self.engine_sound:
            self.engine_sound.stop()
    
    def turn(self, direction):
        if self.speed > 0:
            new_x = self.car_x + direction * self.handling * (self.speed / self.max_speed)
            min_x = self.road_left + 10
            max_x = self.road_left + self.road_width - self.car_width - 10
            self.car_x = max(min_x, min(new_x, max_x))
    
    def update(self, dt):
        if self.game_over:
            return
        
        # التحكم بالميلان
        if self.control_type == 'tilt':
            try:
                from plyer import accelerometer
                accelerometer.enable()
                accel = accelerometer.acceleration
                if accel[0] < -1:  # ميل لليسار
                    self.turn(-1)
                elif accel[0] > 1:  # ميل لليمين
                    self.turn(1)
            except:
                pass
        
        # تحديث السرعة
        if self.speed > 0:
            self.coast()
        
        # تحديث الخصوم
        for opponent in self.opponents[:]:
            opponent['y'] -= self.speed
            if opponent['y'] < -self.car_height:
                self.opponents.remove(opponent)
                self.score += 10
        
        # تحديث العقبات
        for obstacle in self.obstacles[:]:
            obstacle['y'] -= self.speed
            if obstacle['y'] < -50:
                self.obstacles.remove(obstacle)
                self.score += 5
            
            # التحقق من التصادم
            obstacle_rect = [obstacle['x'], obstacle['y'], 50, 50]
            car_rect = [self.car_x, self.car_y, self.car_width, self.car_height]
            
            if self.check_collision(obstacle_rect, car_rect):
                if obstacle['type'] == 'oil':
                    self.speed = min(self.speed * 1.3, self.max_speed * 1.3)
                else:
                    if self.crash_sound:
                        self.crash_sound.play()
                    self.speed = max(self.speed / 2, 1)
                    self.score = max(0, self.score - 20)
                self.obstacles.remove(obstacle)
        
        # إضافة عقبات جديدة
        if random.random() < self.obstacle_frequency:
            obstacle_type = random.choice(['cone', 'barrier', 'oil'])
            lane = random.randint(0, 3)
            x = self.road_left + 50 + lane * (self.road_width - 100) / 3
            self.obstacles.append({
                'type': obstacle_type,
                'x': x,
                'y': Window.height + 100
            })
        
        # إضافة خصوم جدد
        if len(self.opponents) < 3 and random.random() < 0.01:
            lane = random.randint(0, 3)
            x = self.road_left + 50 + lane * (self.road_width - 100) / 3
            speed = random.uniform(
                self.difficulty_settings[self.difficulty]['opponent_speed'] * 0.8,
                self.difficulty_settings[self.difficulty]['opponent_speed'] * 1.2
            )
            self.opponents.append({
                'x': x,
                'y': Window.height + 200,
                'speed': speed,
                'color': random.choice([
                    (0, 0, 1), (0, 1, 0), (1, 1, 0), (1, 0.5, 0)
                ])
            })
        
        # تحديث الخصوم
        for opponent in self.opponents:
            opponent['y'] -= opponent['speed']
        
        # زيادة النقاط بناء على السرعة
        self.score += int(self.speed / 5)
        
        # التحقق من إكمال اللفة
        if self.speed > 0 and self.car_y < Window.height * 0.1:
            self.laps += 1
            self.car_y = Window.height * 0.8
            if self.laps >= self.max_laps:
                self.win_game()
        
        # تحديث سرعة المحرك
        if self.engine_sound:
            self.engine_sound.volume = config.get_setting('sound_volume') * (0.5 + 0.5 * self.speed / self.max_speed)
        
        # إعادة رسم الطريق
        self.canvas.clear()
        self.draw_road()
        self.draw_obstacles()
        self.draw_opponents()
        self.draw_car()
        
        # تحديث عداد السرعة
        self.speedometer.speed = self.speed
        
        # تحديث النتيجة
        self.speedometer.score = self.score
        self.speedometer.laps = self.laps
    
    def draw_car(self):
        with self.canvas:
            Color(1, 0, 0)  # لون السيارة (أحمر)
            Rectangle(
                pos=(self.car_x, self.car_y),
                size=(self.car_width, self.car_height)
            )
            
            # زجاج أمامي
            Color(0.7, 0.7, 1, 0.5)
            Rectangle(
                pos=(self.car_x + self.car_width * 0.2, self.car_y + self.car_height * 0.6),
                size=(self.car_width * 0.6, self.car_height * 0.2)
            )
            
            # عجلات
            Color(0.1, 0.1, 0.1)
            wheel_size = self.car_width * 0.15
            # العجلات الأمامية
            Ellipse(
                pos=(self.car_x + self.car_width * 0.1, self.car_y + self.car_height * 0.1),
                size=(wheel_size, wheel_size)
            )
            Ellipse(
                pos=(self.car_x + self.car_width * 0.75, self.car_y + self.car_height * 0.1),
                size=(wheel_size, wheel_size)
            )
            # العجلات الخلفية
            Ellipse(
                pos=(self.car_x + self.car_width * 0.1, self.car_y + self.car_height * 0.7),
                size=(wheel_size, wheel_size)
            )
            Ellipse(
                pos=(self.car_x + self.car_width * 0.75, self.car_y + self.car_height * 0.7),
                size=(wheel_size, wheel_size)
            )
    
    def draw_opponents(self):
        for opponent in self.opponents:
            with self.canvas:
                Color(*opponent['color'])
                Rectangle(
                    pos=(opponent['x'], opponent['y']),
                    size=(self.car_width, self.car_height)
                )
    
    def draw_obstacles(self):
        for obstacle in self.obstacles:
            with self.canvas:
                if obstacle['type'] == 'cone':
                    Color(1, 0.5, 0)  # برتقالي
                    points = [
                        obstacle['x'] + 25, obstacle['y'] + 50,
                        obstacle['x'], obstacle['y'],
                        obstacle['x'] + 50, obstacle['y']
                    ]
                    Triangle(points=points)
                elif obstacle['type'] == 'barrier':
                    Color(1, 0, 0)  # أحمر
                    Rectangle(
                        pos=(obstacle['x'], obstacle['y']),
                        size=(50, 20)
                    )
                else:  # oil
                    Color(0.1, 0.1, 0.1)  # أسود
                    Ellipse(
                        pos=(obstacle['x'], obstacle['y']),
                        size=(50, 50)
                    )
    
    def check_collision(self, rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def win_game(self):
        self.game_over = True
        if self.engine_sound:
            self.engine_sound.stop()
        
        popup = Popup(
            title='تهانينا!',
            content=Label(text=f'فزت بالسباق!\nنتيجتك: {self.score}'),
            size_hint=(0.8, 0.4)
        )
        popup.open()
        
        # العودة إلى القائمة بعد 3 ثوان
        Clock.schedule_once(lambda dt: self.return_to_menu(), 3)
    
    def game_over(self):
        self.game_over = True
        if self.engine_sound:
            self.engine_sound.stop()
        
        popup = Popup(
            title='انتهت اللعبة',
            content=Label(text=f'تحطمت سيارتك!\nنتيجتك: {self.score}'),
            size_hint=(0.8, 0.4)
        )
        popup.open()
        
        # العودة إلى القائمة بعد 3 ثوان
        Clock.schedule_once(lambda dt: self.return_to_menu(), 3)
    
    def return_to_menu(self):
        self.manager.current = 'start'

# عداد السرعة
class Speedometer(BoxLayout):
    speed = NumericProperty(0)
    score = NumericProperty(0)
    laps = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(Speedometer, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (150, 150)
        self.pos_hint = {'right': 1, 'top': 1}
        self.padding = 10
        self.spacing = 5
        
        with self.canvas:
            Color(0, 0, 0, 0.7)
            Ellipse(pos=self.pos, size=self.size)
        
        self.speed_label = Label(
            text='0 km/h',
            font_size=20,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.5)
        )
        
        self.score_label = Label(
            text='النقاط: 0',
            font_size=16,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.25)
        )
        
        self.laps_label = Label(
            text='اللفات: 0/3',
            font_size=16,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.25)
        )
        
        self.add_widget(self.speed_label)
        self.add_widget(self.score_label)
        self.add_widget(self.laps_label)
    
    def on_speed(self, instance, value):
        self.speed_label.text = f'{int(value * 10)} km/h'
    
    def on_score(self, instance, value):
        self.score_label.text = f'النقاط: {value}'
    
    def on_laps(self, instance, value):
        self.laps_label.text = f'اللفات: {value}/3'

# مدير الشاشات
class GameScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(GameScreenManager, self).__init__(**kwargs)
        self.add_widget(StartScreen(name='start'))
        self.add_widget(SettingsScreen(name='settings'))
        self.add_widget(HelpScreen(name='help'))
        self.add_widget(RacingGame(name='game'))

# التطبيق الرئيسي
class FormulaRacingApp(App):
    def build(self):
        # تعيين خلفية التطبيق
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        return GameScreenManager()

# تشغيل التطبيق
if __name__ == '__main__':
    FormulaRacingApp().run()
