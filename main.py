import flet as ft
import json
import random
import unicodedata
def WriteToFile(filename,data):
    f = open(filename, "w")
    json.dump(data, f,indent=2)
    f.close()
def LoadFromFile(filename):
    f = open(filename,"r")
    data = json.load(f)
    f.close()
    return data

def main(page:ft.Page):
    page.title = "LSHSS Survey"
    page.theme_mode = "light"
    page.theme = ft.Theme(color_scheme_seed="#FF9977AA")
    def show_about(e):
        dlg = ft.AlertDialog(
            title=ft.Text("This app was created by \n"
                          "LSHSS"),
        )
        page.open(dlg)

    def CreateAppBar():
        app_bar = ft.AppBar(
            leading=ft.Image(src="images/csc_logo_80.png"),
            leading_width=100,
            title=ft.Text("LSHSS Survey"),
            #center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.QUESTION_MARK, on_click=show_about),
            ],
        )
        return app_bar
    def chart_badge(icon, size):

        return ft.Container(
            ft.Text(unicodedata.lookup(icon),size=size/2.1, text_align="center",),
            padding=ft.padding.only(top=2),
            width=size,
            height=size,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=size / 2,
            bgcolor=ft.colors.SECONDARY_CONTAINER,
            tooltip=icon
        )
    def get_chart():
        i = 0
        piechart = ft.PieChart(center_space_radius=0)
        for choices in survey_data["choices"]:
            piechart.sections.append(ft.PieChartSection(
                value=choices[1],
                radius = 200,
                title = choices[1],
                title_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                color=ft.colors.random_color(),
                badge = chart_badge(choices[2],50),
                badge_position = 0.98
            ))
            i += 1
        return piechart
    def new_response_clicked(e):
        btn_submit.disabled= False
        btn_new_response.disabled=True
        radio_group.value = -1
        #row_reward.visible = False
        txt_reward.scale = 0
        icon_reward.scale = 0
        icon_reward.rotation = 0
        page.update()
        pass
    def show_reward():
        txt_reward.scale = 1
        icon_reward.content.value = random.choice(rewards)
        icon_reward.rotate += 3.14 * 2
        icon_reward.scale = 1
    def submit_clicked(e):
        if radio_group.value is not None:
            idx = int(radio_group.value)
            survey_data["choices"][idx][1] += 1
            chart_main.sections[idx].value += 1
            chart_main.sections[idx].title = chart_main.sections[idx].value
            WriteToFile(filename,survey_data)
            btn_submit.disabled = True
            btn_new_response.disabled = False
            show_reward()
            page.update()

    filename = "data\\transport.txt"
    rewards = ["✏️","🖊️","🍬"]
    survey_data = LoadFromFile(filename)
    i = 0
    print(page.width)
    radio_cols = ft.Column(spacing=20)
    for choices in survey_data["choices"]:
        radio_cols.controls.append(
            ft.Radio(value=i,label = choices[0] + "\t" + unicodedata.lookup(choices[2])))
        i += 1

    txt_question = ft.Text(value=survey_data["question"], size=24)
    radio_group = ft.RadioGroup( content=radio_cols)
    btn_submit = ft.ElevatedButton(text="Submit", on_click=submit_clicked)
    btn_new_response = ft.ElevatedButton(text="New", disabled=True, on_click=new_response_clicked)
    chart_main = get_chart()
    txt_reward = ft.Text("Thank You for your response. You win", animate_scale=300, scale=0)
    icon_reward = ft.Container(content = ft.Text("🖊️", size=30), animate_rotation=300,rotate=0,scale=0,animate_scale=300)
    row_reward = ft.Row(controls=[txt_reward,icon_reward], visible=True)

    left_col = ft.Column(controls=[txt_question,radio_group,ft.Row(controls=[btn_submit,btn_new_response]), row_reward])
    right_col = ft.Column(controls=[chart_main],expand=True)
    page.add(CreateAppBar(), ft.Container(content=ft.Row(controls=[left_col, right_col]),margin=ft.margin.only(top=10,left=60)))
    page.update()
#ft.app(main)
ft.app(main,view=ft.AppView.WEB_BROWSER)