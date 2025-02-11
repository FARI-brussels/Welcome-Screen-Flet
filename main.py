import flet as ft
from flet import RoundedRectangleBorder, BorderSide
from fletcarousel import BasicHorizontalCarousel
from screeninfo import get_monitors
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import argparse

global language, driver, imageURL, appURL, DEMO_ID, current_route, lst_image_caroussel, lst_image_sdg
DIRECTUS_URL = "https://fari-cms.directus.app"
language = "en"
driver = None
lst_image_caroussel = []
lst_image_sdg = []


def main(page: ft.Page):
    txt_title = ft.Text(value="", color="#2250c6", size=45, font_family="Rhetorik", width=700)
    txt_title_w = ft.Text(value="", color="#ffffff", size=45, font_family="Rhetorik", width=700)
    txt_topic = ft.Text(value="", color="#65C0B5", size=16, font_family="Plain")
    txt_research_head = ft.Text(value="", color="#000000", size=12, font_family="Plain")
    txt_research_lead = ft.Text(value="", color="#000000", size=12, font_family="Plain")
    txt_explain1 = ft.Text(value="", color="#1A202C", font_family="Plain", size=14, width=700)
    txt_start_demo = ft.Text(value="", color="#ffffff", size=28, font_family="Plain")
    txt_explain2 = ft.Text(width=700, value="", color="#ffffff", font_family="Plain", size=14)
    txt_learnmore = ft.ElevatedButton(
        text="",
        icon=ft.icons.LINK_ROUNDED,
        icon_color="#ffffff",
        on_click=lambda _: more(_),
        style=ft.ButtonStyle(
            color="#ffffff",
            padding=10,
            bgcolor={ft.MaterialState.DEFAULT: "#2153d1", ft.MaterialState.HOVERED: ft.colors.BLUE},
            side={
                ft.MaterialState.DEFAULT: BorderSide(1, ft.colors.BLUE),
                ft.MaterialState.HOVERED: BorderSide(2, ft.colors.BLUE),
            },
            overlay_color=ft.colors.TRANSPARENT,
            elevation={"pressed": 0, "": 1},
            animation_duration=500,
            shape={
                ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=50),
            },
        ),
    )

    def changeText():
        """Change the text language based on a given input string (en, nl or fr)"""
        global language, imageURL, appURL, DIRECTUS_URL, lst_image_caroussel, lst_image_sdg
        
        print("[+] Getting data from Directus")
        url = f"{DIRECTUS_URL}/items/demos"
        params = {
            "fields": "*.*",  # Fetch all fields including translations
        }
        
        response = requests.get(url, params=params)
        if not response.ok:
            print(f"Error fetching data: {response.status_code}")
            return
            
        response_json = response.json()
        
        demo_content = next((demo for demo in response_json['data'] if demo['id'] == DEMO_ID), None)
        if not demo_content:
            print(f"Demo with ID {DEMO_ID} not found")
            return

        # Update text content based on language
        translations = demo_content.get('translations', [])
        print(language)
        current_translation = next((t for t in translations if t['languages_code'] == language), None)
        
        if current_translation:
            txt_title.value = current_translation.get('title', '')
            txt_title_w.value = current_translation.get('title', '')
            txt_topic.value = current_translation.get('topic', '')
            txt_explain1.value = current_translation.get('description', '')
            txt_start_demo.value = "start demo"
            txt_explain2.value = ""
            txt_learnmore.text = "learn more"
            txt_research_head.value = demo_content.get('research_head', '')
            txt_research_lead.value = demo_content.get('research_lead', '')

        # Update app URL and images
        appURL = current_translation.get('app_url', '')
        print(demo_content)
        # Handle main image
        if 'image' in demo_content and demo_content['image']:
            imageURL = f"{DIRECTUS_URL}/assets/{demo_content['image']['id']}"
            print(imageURL)
        # Handle carousel images
        if 'logos' in demo_content:
            for logo in demo_content['logos']:
                carousel_img_url = f"{DIRECTUS_URL}/assets/{logo['directus_files_id']}"
                print(carousel_img_url)
                lst_image_caroussel.append(
                    ft.Container(
                        height=50,
                        width=300,
                        content=ft.Image(
                            src=carousel_img_url,
                            fit=ft.ImageFit.FIT_HEIGHT,
                            color="#c5c5c5",
                            height=50,
                        ),
                    )
                )

        # Handle SDG images
        if 'sdg_images' in demo_content:
            for sdg in demo_content['sdg_images']:
                sdg_img_url = f"{DIRECTUS_URL}/assets/{sdg['directus_files_id']}"
                lst_image_sdg.append(
                    ft.Image(
                        src=sdg_img_url,
                        fit=ft.ImageFit.FIT_HEIGHT,
                        height=40,
                    )
                )


    def loadLang():
        """Base on the value of the global var 'language', it load the set of text in the correct language
        """
        changeText()
    
    def more(e):
        """Display the About page (About FARI)

        Args:
            e (error): Should not occur, trust me
        """
        global language
        closeDemo(e)
        page.go('/more')
        pass
    
    def home(e):
        """Display the Home page (Main page with the a explaination of the demo)

        Args:
            e (error): Should not occur, trust me
        """
        global language
        language=e
        loadLang()
        page.go("/home")   

    def demo(e):
        """Display the Demo page (Back page: Close and top bar & Front page: The Selenium demo) 

        Args:
            e (error): Should not occur, trust me
        """
        global driver, appURL
        page.go("/demo")
        options = Options()
        URL = "--app=" + appURL
        options.add_argument(URL)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("silent-debugger-extension-api")
        options.add_argument("no-default-browser-check")
        options.add_argument("disable-windows10-custom-titlebar")
        options.add_argument("disable-auto-maximize-for-tests")
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1920, 980)
        driver.set_window_position(0, 120, windowHandle='current')
        
    def closeDemo(e):
        """Close the Front demo page (Selenium)

        Args:
            e (error): Should not occur, trust me
        """
        global driver
        try:
            driver.close()
            driver = None
        except:
            print("[!] - Error while closing demo")
            #page.go("/home")


    def back(e):
        global language
        closeDemo(e)
        page.go("/home")
    
    def view_pop(view):
        """Change the current view

        Args:
            view (Flet view): New view
        """
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    
    #===============================================================================
    # UIX & GUI DEFINITION
    #===============================================================================  
    def route_change(route):
        """Display the correct page based on the route choose by the user ("/", "/demo", "/how", "/about")

        Args:
            route (string): The URL of the desired page
        """  
        global imageURL, current_route, lst_image_caroussel, lst_image_sdg
        current_route = route
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                bgcolor= "#2250c6",
                controls=
                [   
                    ft.Container(
                            margin=(250),
                            alignment=ft.alignment.center,
                            content=       
                                ft.Column(
                                    spacing=(100),
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Row(
                                            [
                                                ft.Text(value="Choose your language to continue", color="#ffffff", size=30, font_family="Rhetorik")
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                        ft.Row(
                                            spacing=(120),
                                            controls=
                                            [
                                                ft.OutlinedButton(
                                                    width=280,
                                                    content=ft.Container(
                                                    border_radius=50,
                                                    content=ft.Row(
                                                        spacing=(20),
                                                        controls=
                                                        [
                                                            ft.Image(
                                                                src=f"/img/gb.png",
                                                                fit=ft.ImageFit.FIT_HEIGHT,
                                                                height=50,
                                                                width=50,
                                                                border_radius=25,
                                                            ),
                                                            ft.Text(value="English", color="#ffffff", size=20, font_family="Plain")
                                                        ],
                                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                                    ),),
                                                    style=
                                                    ft.ButtonStyle(
                                                        padding=20,
                                                        bgcolor={ft.MaterialState.DEFAULT: "#2153d1", ft.MaterialState.HOVERED: ft.colors.BLUE},
                                                        side={
                                                            ft.MaterialState.DEFAULT: BorderSide(1, ft.colors.BLUE),
                                                            ft.MaterialState.HOVERED: BorderSide(2, ft.colors.BLUE),
                                                        },
                                                        overlay_color=ft.colors.TRANSPARENT,
                                                        elevation={"pressed": 0, "": 1},
                                                        animation_duration=500,
                                                        shape={
                                                            ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=50),
                                                        },
                                                    ),
                                                    data = "en",
                                                    on_click=lambda e: home(e.control.data),
                                                ),
                                                ft.OutlinedButton(
                                                    width=280,
                                                    content=ft.Container(
                                                    border_radius=50,
                                                    content=ft.Row(
                                                        spacing=(20),
                                                        controls=
                                                        [
                                                            ft.Image(
                                                                src=f"/img/nl.png",
                                                                fit=ft.ImageFit.FIT_HEIGHT,
                                                                height=50,
                                                                width=50,
                                                                border_radius=25,
                                                            ),
                                                            ft.Text(value="Nederlands", color="#ffffff", size=20, font_family="Plain")
                                                        ],
                                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                                    ),),
                                                    style=
                                                    ft.ButtonStyle(
                                                        padding=20,
                                                        bgcolor={ft.MaterialState.DEFAULT: "#2153d1", ft.MaterialState.HOVERED: ft.colors.BLUE},
                                                        side={
                                                            ft.MaterialState.DEFAULT: BorderSide(1, ft.colors.BLUE),
                                                            ft.MaterialState.HOVERED: BorderSide(2, ft.colors.BLUE),
                                                        },
                                                        overlay_color=ft.colors.TRANSPARENT,
                                                        elevation={"pressed": 0, "": 1},
                                                        animation_duration=500,
                                                        shape={
                                                            ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=50),
                                                        },
                                                    ),
                                                    data = "nl",
                                                    on_click=lambda e: home(e.control.data),
                                                ),
                                                ft.OutlinedButton(
                                                    width=280,
                                                    content=ft.Container(
                                                    border_radius=50,
                                                    content=ft.Row(
                                                        spacing=(20),
                                                        controls=
                                                        [
                                                            ft.Image(
                                                                src=f"/img/fr.png",
                                                                fit=ft.ImageFit.FIT_HEIGHT,
                                                                height=50,
                                                                width=50,
                                                                border_radius=25,
                                                            ),
                                                            ft.Text(value="Français", color="#ffffff", size=20, font_family="Plain")
                                                        ],
                                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                                    ),),
                                                    style=
                                                    ft.ButtonStyle(
                                                        padding=20,
                                                        bgcolor={ft.MaterialState.DEFAULT: "#2153d1", ft.MaterialState.HOVERED: ft.colors.BLUE},
                                                        side={
                                                            ft.MaterialState.DEFAULT: BorderSide(1, ft.colors.BLUE),
                                                            ft.MaterialState.HOVERED: BorderSide(2, ft.colors.BLUE),
                                                        },
                                                        overlay_color=ft.colors.TRANSPARENT,
                                                        elevation={"pressed": 0, "": 1},
                                                        animation_duration=500,
                                                        shape={
                                                            ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=50),
                                                        },
                                                    ),
                                                    data = "fr",
                                                    on_click=lambda e: home(e.control.data),
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                    ],
                                )
                            
                    )
                ],
            )
        )
        
        if page.route == "/home":
            page.views.append(
                ft.View(
                    "/home",
                    bgcolor="#FFFFFF",
                    controls=
                    [
                        ft.Row(
                            controls=[
                                ft.TextButton(icon=ft.icons.ARROW_BACK, icon_color="#2250c6", on_click=lambda _: page.go("/")),
                                ft.TextButton(
                                    text=language, 
                                    icon=ft.icons.LANGUAGE, 
                                    icon_color="#575757", 
                                    on_click=lambda _: page.go("/"),
                                    style=ft.ButtonStyle(
                                        color="#575757",
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        padding=10,
                                        bgcolor={ft.MaterialState.HOVERED: "#e4e4e4", ft.MaterialState.DEFAULT: "#e4e4e4"},
                                    ),
                                ),     
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Container(
                            margin=(130),
                            alignment=ft.alignment.center,
                            content=
                            ft.Row(
                                spacing=(40),
                                controls=[
                                ft.Column(
                                    spacing=(20),
                                    width=700,
                                    controls=[
                                        txt_title,
                                        ft.Column(
                                            spacing=(5),
                                            controls=[
                                                ft.Row(
                                                    spacing=20,
                                                    controls=[
                                                        ft.Text(value="Research head:", weight=ft.FontWeight.BOLD,color="#000000", size=12, font_family="Plain"),
                                                        txt_research_head,
                                                    ]
                                                ),
                                                ft.Row(
                                                    spacing=20,
                                                    controls=[
                                                        ft.Text(value="Lead researcher(s):", weight=ft.FontWeight.BOLD,color="#000000", size=12, font_family="Plain"),
                                                        txt_research_lead,
                                                    ]
                                                ),
                                            ]
                                        ),
                                        ft.Row(
                        
                                            controls=[
                                                txt_topic,
                                                ft.Row(
                                                    spacing=10,
                                                    controls=lst_image_sdg,
                                                ),
                                                
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                        ),
                                        txt_explain1,
                                        txt_learnmore,
                                    ],
                                    #alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.ElevatedButton(
                                    content=
                                    ft.Container(
                                        border_radius=50,
                                        content=ft.Row(
                                            spacing=(20),
                                            controls=
                                            [
                                                txt_start_demo,
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                        ),
                                    ),
                                    style=ft.ButtonStyle(
                                        shape=ft.CircleBorder(), 
                                        padding=180,
                                        bgcolor={ft.MaterialState.DEFAULT: "#2250c6", ft.MaterialState.HOVERED: ft.colors.BLUE},
                                        side={
                                            ft.MaterialState.DEFAULT: BorderSide(1, "#2250c6"),
                                            ft.MaterialState.HOVERED: BorderSide(4, ft.colors.BLUE),
                                        },
                                    ),
                                    on_click=demo
                                ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ), 
                        ft.Container(
                            height=100,
                        ),
                        ft.Container(
                            alignment=ft.alignment.bottom_center,
                            border={
                                ft.MaterialState.DEFAULT: BorderSide(1, ft.colors.BLUE_GREY),
                                ft.MaterialState.HOVERED: BorderSide(2, ft.colors.BLUE_GREY),
                            },
                            content=
                            ft.Column(
                                controls=[
                                    ft.Divider(height=9, thickness=1, color="#C6C6C6"),
                                    ft.Container(
                                        height=20,
                                    ),
                                    ft.Row(
                                        spacing=(40),
                                        controls=[
                                            BasicHorizontalCarousel(
                                                page=page,
                                                items_count=5,
                                                #auto_cycle=AutoCycle(duration=1),
                                                items=lst_image_caroussel,
                                                buttons=[
                                                    ft.TextButton(
                                                        icon=ft.icons.NAVIGATE_BEFORE,
                                                        icon_color="#2250c6"
                                                    ),
                                                    ft.TextButton(
                                                        icon=ft.icons.NAVIGATE_NEXT,
                                                        icon_color="#2250c6"
                                                    )
                                                ],
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                items_alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        
                                    )
                                    
                                ]
                            ),
                        )
                    ],
                )
            )
        if page.route == "/more":
            page.views.append(
                ft.View(
                    "/more",
                    bgcolor= "#2250c6",
                    controls=
                    [
                        ft.Row(
                            controls=[
                                ft.TextButton(
                                    icon=ft.icons.ARROW_BACK, 
                                    icon_color="#ffffff", 
                                    on_click=lambda _: page.go("/home"),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        padding=10,
                                    ),
                                ),    
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Container(
                            margin=(130),
                            alignment=ft.alignment.center,
                            content=
                            ft.Row(
                                spacing=(70),
                                controls=[
                                ft.Column(
                                    spacing=(20),
                                    controls=[
                                        txt_title_w,
                                        txt_topic,
                                        txt_explain2,    
                                    ],
                                    
                                ),
                                ft.Image(
                                    src=imageURL,
                                    fit=ft.ImageFit.COVER,
                                    width=700,
                                ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),
                        
                    ],
                )
            )
        
        if page.route == "/demo":
            page.views.append(
                ft.View(
                    "/demo",
                    bgcolor="#2250c6",
                    controls=
                    [
                        ft.Row(
                            height=100,
                            controls=[
                                ft.TextButton(icon=ft.icons.ARROW_BACK, icon_color="#ffffff", on_click=lambda _: back(_)),
                                ft.Image(
                                    src=f"/img/logo_w.png",
                                    fit=ft.ImageFit.FIT_HEIGHT,
                                    color="#ffffff",
                                    height=50,
                                ),
                                txt_learnmore,   
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        
                    ]
                )
            )
            
        page.update()

    #===============================================================================
    # MAIN CODE & GLOBAL VAR
    #===============================================================================    
    page.title = "FARI - Welcome screen"
    page.fonts = {
        "Plain": "/fonts/Plain-Regular.otf",
        "Rhetorik": "/fonts/RhetorikSerifTrial-Regular.ttf"
    }
    
    m = get_monitors()
    h = m[0].height
    w = m[0].width
        
    page.window_width = w       
    page.window_height = h
    page.window_resizable = False

    page.update()  
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Running demo welcome page')
    parser.add_argument('--id', required=True, help='the Directus demo ID')
    args = parser.parse_args()
    DEMO_ID = int(args.id)

    ft.app(target=main, view=ft.WEB_BROWSER, port=8550, assets_dir="assets")
    
