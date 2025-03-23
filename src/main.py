import flet as ft
import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import asyncio

from ai import generate_response

async def main(page: ft.Page):
    page.title = "Flet counter example"
    page.bgcolor = '#001c33'

    pygame.mixer.init()

    async def recognition(e):
        microphone_button.icon = ft.Icons.MIC
        page.update()
        await asyncio.sleep(0.1)
        
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='ru-RU')
            microphone_button.icon = ft.Icons.ACCESS_TIME
            page.update()
            await asyncio.sleep(0.1)

            response = await generate_response(text)
            
            tts = gTTS(text=response, lang='ru')
            tts.save('audio.mp3')
            
            pygame.mixer.music.load("audio.mp3")
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            
            pygame.mixer.music.unload()
            os.remove('audio.mp3')

            microphone_button.icon = ft.Icons.MIC_NONE
            page.update()
            await asyncio.sleep(0.1)
            
        except Exception as e:
            microphone_button.icon = ft.Icons.MIC_NONE
            page.update()
            await asyncio.sleep(0.1)
            print("Error:", e)
    
    microphone_button = ft.IconButton(
        icon=ft.Icons.MIC_NONE,
        icon_color="#7d7f7d",
        icon_size=250,
        tooltip="Start recognition",
        bgcolor="#00e5ff",
        on_click=recognition
    )

    # Создаем основной контейнер с Column, занимающий всю высоту
    main_col = ft.Column(
        expand=True,  # Занимает все доступное пространство
        spacing=0,
        controls=[
            # Верхний контейнер с текстом
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(
                            'Charlie Voice Assistant',
                            color='#00f89d',
                            size=50
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                bgcolor='#000453',
                border_radius=10,
                padding=20
            ),
            # Контейнер для кнопки, занимающий оставшееся пространство
            ft.Container(
                expand=True,  # Занимает все оставшееся пространство
                content=ft.Row(
                    controls=[
                        microphone_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ]
    )
    
    page.add(main_col)

ft.app(main, view=ft.AppView.WEB_BROWSER)
