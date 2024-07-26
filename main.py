import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, filedialog, Menu, simpledialog, font
from PIL import Image, ImageTk, ImageSequence, ImageFont, ImageDraw


class AnimatedImageApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Анимированные изображения")
        self.master.geometry("800x800")
        ctk.set_appearance_mode("dark")  # Выберите режим "dark" или "light"
        ctk.set_default_color_theme("blue")  # Выберите цветовую тему

        self.canvas = ctk.CTkCanvas(self.master, width=720, height=720)
        self.canvas.pack(padx=20, pady=20)

        # Первый ряд кнопок
        frame1 = ctk.CTkFrame(self.master)
        frame1.pack(pady=10)
        self.load_button = ctk.CTkButton(frame1, text="Загрузить изображение", command=self.load_image, width=200)
        self.load_button.pack(side=ctk.LEFT, padx=5)

        self.play_button = ctk.CTkButton(frame1, text="Воспроизвести", command=self.toggle_play, width=200)
        self.play_button.pack(side=ctk.LEFT, padx=5)
        self.playing = False

        self.pause_button = ctk.CTkButton(frame1, text="Пауза", command=self.pause_animation, width=200)
        self.pause_button.pack(side=ctk.LEFT, padx=5)

        # Второй ряд кнопок
        frame2 = ctk.CTkFrame(self.master)
        frame2.pack(pady=10)
        self.move_button = ctk.CTkButton(frame2, text="Переместить изображение", command=self.start_move, width=200)
        self.move_button.pack(side=ctk.LEFT, padx=5)

        self.rotate_button = ctk.CTkButton(frame2, text="Вращать изображение", command=self.rotate_image, width=200)
        self.rotate_button.pack(side=ctk.LEFT, padx=5)
        self.rotation_direction_menu = Menu(frame2, tearoff=0)
        self.rotation_direction_menu.add_command(label="По часовой стрелке",
                                                 command=lambda: self.choose_rotation_direction(True))
        self.rotation_direction_menu.add_command(label="Против часовой стрелки",
                                                 command=lambda: self.choose_rotation_direction(False))

        self.scale_menu = Menu(frame2, tearoff=0)
        self.scale_menu.add_command(label="Увеличить", command=lambda: self.scale_image(True))
        self.scale_menu.add_command(label="Уменьшить", command=lambda: self.scale_image(False))
        self.enlarge_button = ctk.CTkButton(frame2, text="Масштабировать", command=self.show_scale_menu, width=200)
        self.enlarge_button.pack(side=ctk.LEFT, padx=5)

        # Третий ряд кнопок
        frame3 = ctk.CTkFrame(self.master)
        frame3.pack(pady=10)
        self.transparent_button = ctk.CTkButton(frame3, text="Прозрачность", command=self.adjust_transparency,
                                                width=200)
        self.transparent_button.pack(side=ctk.LEFT, padx=5)

        self.text_button = ctk.CTkButton(frame3, text="Добавить текст", command=self.add_text, width=200)
        self.text_button.pack(side=ctk.LEFT, padx=5)

        self.font_dropdown = ctk.CTkComboBox(frame3, values=["Arial", "Times New Roman", "Courier New"], width=200)
        self.font_dropdown.pack(side=ctk.LEFT, padx=5)
        self.font_dropdown.set("Arial")

        # Добавляем кнопки для управления анимацией текста в frame4
        frame4 = ctk.CTkFrame(self.master)
        frame4.pack(pady=10)

        self.rotate_text_button = ctk.CTkButton(frame4, text="Вращать текст", command=self.rotate_text, width=200)
        self.rotate_text_button.pack(side=ctk.LEFT, padx=5)

        self.rotation_direction_menu_text = Menu(frame4, tearoff=0)
        self.rotation_direction_menu_text.add_command(label="По часовой стрелке",
                                                      command=lambda: self.choose_rotation_direction(True))
        self.rotation_direction_menu_text.add_command(label="Против часовой стрелки",
                                                      command=lambda: self.choose_rotation_direction(False))

        self.adjust_transparency_button = ctk.CTkButton(frame4, text="Изменить прозрачность текста",
                                                        command=self.show_transparency_menu, width=200)
        self.adjust_transparency_button.pack(side=ctk.LEFT, padx=5)

        self.transparency_menu = Menu(frame4, tearoff=0)
        self.transparency_menu.add_command(label="Увеличить", command=lambda: self.adjust_text_transparency(True))
        self.transparency_menu.add_command(label="Уменьшить", command=lambda: self.adjust_text_transparency(False))

        self.scale_text_button = ctk.CTkButton(frame4, text="Масштабировать текст", command=self.show_scale_text_menu,
                                               width=200)
        self.scale_text_button.pack(side=ctk.LEFT, padx=5)
        self.scale_text_menu = Menu(frame4, tearoff=0)
        self.scale_text_menu.add_command(label="Увеличить", command=lambda: self.scale_text(True))
        self.scale_text_menu.add_command(label="Уменьшить", command=lambda: self.scale_text(False))

        # Добавляем кнопки "Сохранить в GIF" и "Отмена" в frame5
        frame5 = ctk.CTkFrame(self.master)
        frame5.pack(pady=10)

        self.save_button = ctk.CTkButton(frame5, text="Сохранить в GIF", command=self.save_as_gif, width=200)
        self.save_button.pack(side=ctk.LEFT, padx=5)

        self.reset_button = ctk.CTkButton(frame5, text="Отмена", command=self.reset_image, width=200)
        self.reset_button.pack(side=ctk.LEFT, padx=5)

        self.start_image_coords = None

        self.images = []
        self.original_images = []
        self.current_image_index = 0
        self.animation_delay = 1000
        self.animation_job = None

        self.current_image = None
        self.image_position = None
        self.start_coords = None
        self.move_allowed = True
        self.moving = False

        self.rotation_angle = 0
        self.rotation_step = 10
        self.rotation_frames = 36
        self.clockwise_rotation = True

        self.image_scale = 1.0
        self.scale_factor = 0.1
        self.scale_image_increase = True

        self.transparency = 1.0
        self.transparency_factor = 0.1

        self.max_scale = 2.0
        self.min_scale = 0.5

        self.available_fonts = font.families()
        self.add_text_mode = False
        self.selected_font = "Arial"
        self.text_position = (0, 0)
        self.text = None
        self.text_entry = None
        self.edit_text_mode = False  # Флаг для режима редактирования текста
        self.prev_x = None
        self.prev_y = None
        self.rotate_text_job = None

        self.text_objects = {}  # Список для хранения текстовых объектов
        self.last_click_time = 0

        self.canvas.bind("<Button-1>", self.on_press_text)
        self.canvas.bind("<Double-Button-1>", self.edit_text)

        self.rotation_job = None
        self.scaling_job = None
        self.transparency_job = None

        self.image_changes = []

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            self.images.append(image)
            self.original_images.append(image.copy())
            self.display_image()
            self.move_button.config(state=tk.NORMAL)
            self.enlarge_button.config(state=tk.NORMAL)
            self.transparent_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)

    def display_image(self):
        image = self.images[self.current_image_index]
        image.thumbnail((720, 720))
        self.current_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image, tags="image")
        self.image_position = (0, 0)

    def toggle_play(self):
        self.playing = not self.playing
        if self.playing:
            self.play_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.start_animation()
        else:
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.pause_animation()

    def start_animation(self):
        if not self.animation_job:
            self.animation_job = self.master.after(self.animation_delay, self.next_image)

    def next_image(self):
        if self.playing:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.display_image()
            self.animation_job = self.master.after(self.animation_delay, self.next_image)

    def pause_animation(self):
        self.playing = False
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        if self.animation_job:
            self.master.after_cancel(self.animation_job)
            self.animation_job = None

    def start_move(self):
        if self.move_allowed:
            self.canvas.bind("<Button-1>", self.on_press)
            self.canvas.bind("<B1-Motion>", self.on_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_release)
            self.moving = True
            # Установить флаг, разрешающий добавление текста
            self.add_text_mode = True

    def on_press(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]  # Получаем только первый индентификатор
        if "image" in self.canvas.gettags(item):
            self.start_coords = (event.x, event.y)
            self.start_image_coords = self.canvas.coords("image")
            # Сбрасываем флаг, позволяющий создавать текст
            self.add_text_mode = False

    def on_drag(self, event):
        if self.moving and self.start_coords:
            dx = event.x - self.start_coords[0]
            dy = event.y - self.start_coords[1]
            self.canvas.move("image", dx, dy)
            self.start_coords = (event.x, event.y)

    def on_release(self, event):
        self.start_coords = None
        # Устанавливаем флаг, позволяющий создавать текст
        self.add_text_mode = True

    def update_image(self):
        image = self.images[self.current_image_index].copy()

        # Применение вращения
        image = image.rotate(self.rotation_angle)

        # Применение масштабирования
        old_width, old_height = image.size
        new_width = int(old_width * self.image_scale)
        new_height = int(old_height * self.image_scale)
        image = image.resize((new_width, new_height))

        # Применение прозрачности
        alpha = int(255 * self.transparency)
        image.putalpha(alpha)

        self.current_image = ImageTk.PhotoImage(image)
        self.canvas.delete("image")
        self.canvas.create_image(self.image_position[0], self.image_position[1], anchor=tk.NW, image=self.current_image,
                                 tags="image")

    def rotate_image(self):
        self.show_rotation_direction_menu()

        # Отменить предыдущую операцию вращения, если она запущена
        if self.rotation_job:
            self.master.after_cancel(self.rotation_job)

        # Запустить новую операцию вращения
        self.rotation_job = self.master.after(50, self.rotate_image_once)
        # Установить флаг, разрешающий добавление текста
        self.add_text_mode = True
        self.image_changes.append(("rotation", self.rotation_angle))

    def rotate_image_once(self):
        if self.clockwise_rotation:
            self.rotation_angle = (self.rotation_angle + self.rotation_step) % 360
        else:
            self.rotation_angle = (self.rotation_angle - self.rotation_step) % 360

        self.update_image()
        # Запустить новую операцию вращения
        self.rotation_job = self.master.after(50, self.rotate_image_once)

    def show_rotation_direction_menu(self):
        self.rotation_direction_menu.post(self.rotate_button.winfo_rootx(), self.rotate_button.winfo_rooty())

    def choose_rotation_direction(self, clockwise):
        self.clockwise_rotation = clockwise

    def show_scale_menu(self):
        self.scale_menu.post(self.enlarge_button.winfo_rootx(), self.enlarge_button.winfo_rooty())

    def scale_image(self, enlarge=True):
        # Отменить предыдущую операцию масштабирования, если она запущена
        if self.scaling_job:
            self.master.after_cancel(self.scaling_job)
            self.scaling_job = None

        target_scale = self.max_scale if enlarge else self.min_scale
        if self.image_scale != target_scale:
            if self.image_scale < target_scale:
                self.image_scale = min(self.image_scale + 0.01, target_scale)
            else:
                self.image_scale = max(self.image_scale - 0.01, target_scale)
            self.apply_scaling()
            # Запустить новую операцию масштабирования
            self.scaling_job = self.master.after(10, lambda: self.scale_image(enlarge))
        # Установить флаг, разрешающий добавление текста
        self.add_text_mode = True
        self.scale_image_increase = enlarge
        self.image_changes.append(("scaling", self.image_scale))

    def apply_scaling(self):
        self.update_image()

    def adjust_transparency(self):
        # Отменить предыдущую операцию изменения прозрачности, если она запущена
        if self.transparency_job:
            self.master.after_cancel(self.transparency_job)
            self.transparency_job = None

        self.transparency -= self.transparency_factor
        if self.transparency < 0:
            self.transparency = 0

        self.apply_transparency()
        # Запустить новую операцию изменения прозрачности
        self.transparency_job = self.master.after(100, self.adjust_transparency)
        # Установить флаг, разрешающий добавление текста
        self.add_text_mode = True
        self.image_changes.append(("transparency", self.transparency))

    def apply_transparency(self):
        self.update_image()

    def add_text(self):
        if not self.add_text_mode:  # Добавьте проверку на флаг, чтобы избежать множественных нажатий
            self.add_text_mode = True

    def on_press_text(self, event):
        if self.add_text_mode:
            x, y = event.x, event.y
            self.text_position = (x, y)
            # Устанавливаем выбранный шрифт из ComboBox для создаваемого текстового объекта
            selected_font = self.font_dropdown.get()
            self.selected_font = selected_font  # Сохраняем выбранный шрифт
            text_id = self.canvas.create_text(x, y, text="Your Text Here", font=(selected_font, 12), fill="black", anchor="nw")
            self.text_objects[text_id] = (x, y)  # Сохраняем созданный текстовый объект в словаре
            self.canvas.tag_bind(text_id, "<Double-Button-1>", self.edit_text)  # Привязываем редактирование текста
            self.canvas.tag_bind(text_id, "<B1-Motion>", self.on_drag_text)
            self.canvas.tag_bind(text_id, "<ButtonRelease-1>", self.on_release_text)
            self.add_text_mode = False  # Сбросить флаг после создания текста

    def on_drag_text(self, event):
        if not self.edit_text_mode:
            # Получаем id текста, на который нажали
            text_id = event.widget.find_withtag(tk.CURRENT)
            if text_id:
                text_id = text_id[0]
                # Проверяем, есть ли такой текст в словаре text_objects
                if text_id in self.text_objects:
                    # Рассчитываем изменение координат
                    dx = event.x - self.text_position[0]
                    dy = event.y - self.text_position[1]
                    # Перемещаем текст на холсте на соответствующее значение изменения
                    self.canvas.move(text_id, dx, dy)
                    # Обновляем позицию текста в словаре text_objects
                    self.text_objects[text_id] = (
                    self.text_objects[text_id][0] + dx, self.text_objects[text_id][1] + dy)
                    # Обновляем текущую позицию мыши
                    self.text_position = (event.x, event.y)

    def on_release_text(self, event):
        self.add_text_mode = False

    def edit_text(self, event):
        text_id = event.widget.find_withtag(tk.CURRENT)
        if text_id:
            text_id = text_id[0]
            if text_id in self.text_objects:
                self.edit_text_mode = True
                # Получаем текущий текст
                current_text = self.canvas.itemcget(text_id, "text")
                # Получаем текущие координаты текста
                x, y = self.text_objects[text_id]
                # Удаляем существующий текст
                self.canvas.delete(text_id)
                # Создаем поле для ввода с сохраненными координатами текста
                self.text_entry = tk.Entry(self.master, font=(self.selected_font, 12), bg="white", relief="flat")
                self.text_entry.insert(0, current_text)
                self.text_entry.place(x=x, y=y, anchor="nw")
                self.text_entry.focus_set()
                # Привязываем события окончания редактирования
                self.text_entry.bind("<Return>", lambda e: self.finish_edit_text(text_id))
                self.text_entry.bind("<FocusOut>", lambda e: self.finish_edit_text(text_id))

    def finish_edit_text(self, text_id):
        if self.text_entry:
            new_text = self.text_entry.get()
            self.text_entry.destroy()
            self.text_entry = None
            self.edit_text_mode = False
            if new_text:
                # Удаляем старый текст с холста
                self.canvas.delete(text_id)
                # Получаем позицию из словаря text_objects
                x, y = self.text_objects[text_id]
                # Создаем новый текст на холсте с отредактированным текстом
                new_text_id = self.canvas.create_text(x, y, text=new_text, font=(self.selected_font, 12), fill="black",
                                                      anchor="nw")
                # Обновляем позицию нового текста в словаре text_objects
                self.text_objects[new_text_id] = (x, y)
                # Привязываем события редактирования и перемещения к новому тексту
                self.canvas.tag_bind(new_text_id, "<Double-Button-1>", self.edit_text)
                self.canvas.tag_bind(new_text_id, "<B1-Motion>", self.on_drag_text)
                self.canvas.tag_bind(new_text_id, "<ButtonRelease-1>", self.on_release_text)

    def rotate_text(self, clockwise=True, angle_increment=1):
        if not self.edit_text_mode:
            for text_id in self.text_objects:
                self.rotate_text_animation(text_id, clockwise, angle_increment)

    def rotate_text_animation(self, text_id, clockwise=True, angle_increment=1):
        current_angle = 0  # Начальный угол вращения
        while True:  # Бесконечный цикл для непрерывного вращения
            current_angle += angle_increment if clockwise else -angle_increment  # Увеличиваем или уменьшаем угол в зависимости от направления вращения
            self.canvas.itemconfig(text_id, angle=current_angle)  # Устанавливаем новый угол вращения для текста
            self.master.update()  # Обновляем окно для отображения изменений
            self.master.after(50)  # Задержка для создания эффекта плавного вращения

    def adjust_text_transparency(self, increase=True):
        if not self.edit_text_mode:
            for text_id in self.text_objects:
                self.adjust_text_transparency_animation(text_id, increase)

    def adjust_text_transparency_animation(self, text_id, increase=True):
        current_fill_color = self.canvas.itemcget(text_id, "fill")
        current_rgb = self.canvas.winfo_rgb(current_fill_color)

        # Преобразуем значение RGB в диапазон 0-255
        red = current_rgb[0] // 256
        green = current_rgb[1] // 256
        blue = current_rgb[2] // 256

        if increase:
            red = min(255, red + 25)
            green = min(255, green + 25)
            blue = min(255, blue + 25)
        else:
            red = max(0, red - 25)
            green = max(0, green - 25)
            blue = max(0, blue - 25)

        new_fill_color = "#%02x%02x%02x" % (red, green, blue)
        self.canvas.itemconfig(text_id, fill=new_fill_color)

    def show_transparency_menu(self):
        self.transparency_menu.post(self.adjust_transparency_button.winfo_rootx(),
                                    self.adjust_transparency_button.winfo_rooty() + self.adjust_transparency_button.winfo_height())

    def scale_text(self, enlarge=True, scale_factor=1.1):
        if not self.edit_text_mode:
            for text_id in self.text_objects:
                current_font = self.canvas.itemcget(text_id, "font")
                font_family, font_size = current_font.split()
                font_size = int(float(font_size))  # Преобразуем размер шрифта в целое число

                if enlarge:
                    target_font_size = font_size * 2  # Увеличиваем размер шрифта вдвое
                else:
                    target_font_size = font_size // 2  # Уменьшаем размер шрифта вдвое

                self.animate_scale(text_id, font_family, font_size, target_font_size)

    def animate_scale(self, text_id, font_family, font_size, target_font_size):
        if font_size != target_font_size:
            if font_size < target_font_size:
                font_size = min(font_size + 1, target_font_size)
            else:
                font_size = max(font_size - 1, target_font_size)

            new_font = (font_family, font_size)
            self.canvas.itemconfig(text_id, font=new_font)
            self.master.after(100, lambda: self.animate_scale(text_id, font_family, font_size, target_font_size))

    def show_scale_text_menu(self):
        self.scale_text_menu.post(self.scale_text_button.winfo_rootx(),
                             self.scale_text_button.winfo_rooty() + self.scale_text_button.winfo_height())

    def save_as_gif(self):
        filename = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
        if filename:
            frames = []

            # Получаем размеры оригинального изображения
            original_image = self.images[self.current_image_index].copy()
            original_width, original_height = original_image.size

            # Создаем последовательность кадров для GIF
            for frame_number in range(max(self.rotation_frames, 21)):
                image_copy = original_image.copy()

                # Применение вращения
                if "rotation" in [change[0] for change in self.image_changes]:
                    rotation_angle = (self.rotation_angle + self.rotation_step * frame_number) % 360
                    image_copy = image_copy.rotate(rotation_angle)

                # Применение масштабирования
                if "scaling" in [change[0] for change in self.image_changes]:
                    if self.scale_image_increase:
                        scale_factor = 1 + (frame_number - 10) * 0.05  # Изменяем шаг до 5%
                    else:
                        scale_factor = 1 - (frame_number - 10) * 0.05  # Изменяем шаг до 5%
                    new_width = int(original_width * scale_factor)
                    new_height = int(original_height * scale_factor)
                    image_copy = image_copy.resize((new_width, new_height))

                    # Центрируем изображение на холсте
                    new_canvas = Image.new("RGB", (720, 720), (0, 0, 0, 0))
                    new_canvas.paste(image_copy, ((720 - new_width) // 2, (720 - new_height) // 2))
                    image_copy = new_canvas

                    # Применение прозрачности
                if "transparency" in [change[0] for change in self.image_changes]:
                    alpha = int(255 * (1 - frame_number / 20))  # Уменьшаем прозрачность с шагом 5%
                    image_copy = image_copy.convert("RGB")
                    alpha_layer = Image.new("L", image_copy.size, alpha)
                    image_copy.putalpha(alpha_layer)

                frames.append(image_copy)

                # Сохраняем анимацию в GIF
                frames[0].save(filename, save_all=True, append_images=frames[1:], loop=0, duration=50)

    def reset_image(self):
        # Отменяем асинхронные вызовы методов, если они существуют
        if self.rotation_job:
            self.master.after_cancel(self.rotation_job)
            self.rotation_job = None

        if self.scaling_job:
            self.master.after_cancel(self.scaling_job)
            self.scaling_job = None

        if self.transparency_job:
            self.master.after_cancel(self.transparency_job)
            self.transparency_job = None

        # Сбрасываем параметры
        self.image_scale = 1.0
        self.transparency = 1.0
        self.rotation_angle = 0

        # Возвращаем изображение к исходному состоянию
        self.images = self.original_images[:]
        self.current_image_index = 0
        self.display_image()

        # Устанавливаем флаг move_allowed в True после сброса изображения
        self.move_allowed = True

        self.add_text_mode = True
        # Блокируем перемещение изображения
        self.moving = False


def main():
    root = tk.Tk()
    app = AnimatedImageApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
