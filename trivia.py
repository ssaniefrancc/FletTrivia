import flet as ft
import time
import threading
from db import questions

class TriviaGame(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.current_question = 0
        self.score = 0
        self.timer = 15
        self.timer_running = False  # temporizador detenido al inicio pa evitar conflictos
        self.game_started = False

    def build(self):
        #elementos de la interfaz
        self.question_text = ft.Text(value="PREGUNTA", size=24, text_align="center", color="white", visible=False)
        
        #botones de opcion
        self.option_buttons = [
            ft.ElevatedButton(
                text="Option",
                on_click=self.check_answer,
                color="cyan",
                width=120,
                height=50,  
                visible=False
            ) for _ in range(4)
        ]
        
        self.timer_text = ft.Text(value=f"⏰ {self.timer} sec", size=18, color="red", visible=False)
        self.start_button = ft.ElevatedButton(text="Comenzar", on_click=self.start_game, width=200, height=50, color="green")
        self.restart_button = ft.ElevatedButton(text="Reiniciar", on_click=self.restart_game, width=200, height=50, color="orange", visible=False)

        # layout :)
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        [self.timer_text],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    self.question_text,
                    ft.GridView(
                        controls=self.option_buttons,
                        runs_count=2,  # para definir la cantidad de columnas, la cuadricula de 2x2
                        spacing=10,
                        run_spacing=10,
                    ),
                    ft.Container(
                        content=self.start_button,
                        alignment=ft.alignment.center,
                    ),
                    self.restart_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
        )

    def load_question(self):
        # cargar pregunta
        question_data = questions[self.current_question]
        self.question_text.value = question_data["question"]
        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].text = option
        self.update()

    def check_answer(self, e):
        # verificar si la respuesta es correcta
        selected_option = e.control.text
        correct_answer = questions[self.current_question]["answer"]
        if selected_option == correct_answer: #agregar el puntaje en caso de que la respuesta sea correcta
            self.score += 1
        self.next_question()

    def next_question(self):
        # pasar a la siguiente pregunta
        self.current_question += 1
        if self.current_question < len(questions):
            self.load_question()
            self.timer = 15  # reiniciar temporizador
            self.timer_running = True
            threading.Thread(target=self.update_timer).start()  # iniciar nuevamente el temporizador para que no quede en 0
        else:
            self.end_game()

    def end_game(self):
        # resultado final de la partida
        self.question_text.value = f"Fin del juego! Tu puntuación es: {self.score}/{len(questions)}"
        for btn in self.option_buttons:
            btn.visible = False
        self.timer_running = False
        self.timer_text.visible = False  # se usa para ocultar el temporizador cuando se termine la partida
        self.restart_button.visible = True  # mostrar boton de reinicio para volver a jugar
        self.update()

    def update_timer(self):
        # actualizar el temporizador
        while self.timer_running and self.timer > 0:
            time.sleep(1)
            self.timer -= 1
            self.timer_text.value = f"⏰ {self.timer} s"
            self.update()
        if self.timer == 0 and self.timer_running:
            self.timer_running = False  # parar el temporizador cuando llegue a 0
            self.next_question()  # para cambiar de pregunta cuando finalice el tiempo

    def start_game(self, e=None):
        # Iniciar juego
        self.start_button.visible = False
        self.restart_button.visible = False
        self.current_question = 0
        self.score = 0
        self.timer = 15
        self.timer_text.value = f"⏰ {self.timer} s"  # reiniciar el valor del temporizador
        self.timer_text.visible = True  # mostrar el temporizador nuevamente
        self.timer_running = True
        self.game_started = True

        # hacer visible los contenedores necesarios
        self.question_text.visible = True
        for btn in self.option_buttons:
            btn.visible = True

        self.load_question()
        threading.Thread(target=self.update_timer).start()
        self.update()

    def restart_game(self, e=None):
        # reiniciar
        self.start_game()

def main(page: ft.Page):
    page.title = "Juego de Trivia"
    page.window_width = 550
    page.window_height = 750
    page.window_resizable = False  # no autorizo ajustar tamaño
    game = TriviaGame()
    page.add(game)

ft.app(target=main)
