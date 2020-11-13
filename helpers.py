lusername_input = """
MDTextField:
    hint_text: "Enter username"
    helper_text: "Enter the full name"
    helper_text_mode: "on_focus"
    required: True
    icon_right: "human"
    icon_right_color: [1,1,1,1]
    pos_hint:{'center_x': 0.5, 'center_y': 0.5}
    size_hint_x:None
    width:250
"""
lpassword_input ="""
MDTextField:
    hint_text: "Enter password"
    helper_text: "Check if caps lock is on"
    helper_text_mode: "on_focus"
    password: True
    required: True
    icon_right: "lock-outline"
    icon_right_color: [1,1,1,1]
    pos_hint:{'center_x': 0.5, 'center_y': 0.4}
    size_hint_x:None
    width:250
"""



username_input = """
MDTextField:
    hint_text: "Enter username"
    helper_text: "Enter the full name"
    helper_text_mode: "on_focus"
    required: True
    icon_right: "human"
    icon_right_color: [1,1,1,1]
    pos_hint:{'center_x': 0.5, 'center_y': 0.7}
    size_hint_x:None
    width:250
"""
mycontact_input = """
MDTextField:
    hint_text: "Enter contact number"
    helper_text: "Number must contain 10 digits"
    helper_text_mode: "on_focus"
    required: True
    icon_right: "cellphone"
    icon_right_color: [1,1,1,1]
    pos_hint:{'center_x': 0.5, 'center_y': 0.6}
    size_hint_x:None
    width:250
"""
age_input="""
MDTextField:
    hint_text: "Enter age"
    helper_text: "It must be a number"
    helper_text_mode: "on_focus"
    required: True
    icon_right: "number"
    icon_right_color: [1,1,1,1]
    pos_hint:{'center_x': 0.5, 'center_y': 0.5}
    size_hint_x:None
    width:250
"""
email_input = """
MDTextField:
    hint_text: "Enter email id"
    helper_text_mode: "on_focus"
    required: True
    icon_right: "email"
    icon_right_color: [1,1,1,1]
    pos_hint:{'center_x': 0.5, 'center_y': 0.4}
    size_hint_x:None
    width:250
"""
password_input ="""
MDTextField:
    hint_text: "Enter password"
    helper_text: "Password must contain at least 8 letter."
    helper_text_mode: "on_focus"
    password: True
    required: True
    icon_right: "lock-outline"
    icon_right_color: [1,1,1,1]
    pos_hint:{'center_x': 0.5, 'center_y': 0.3}
    size_hint_x:None
    width:250
"""
abusername_input = """
MDTextField:
    hint_text: "Enter abuser name"
    helper_text: "Enter the full name"
    helper_text_mode: "on_focus"
    icon_right: "human"
    icon_right_color: [1,1,1,1]
    pos_hint:{'center_x': 0.5, 'center_y': 0.6}
    size_hint_x:None
    width:250
"""
contact_input = """
MDTextField:
    hint_text: "Enter abusers contact number"
    helper_text: "Number must contain 10 digits"
    helper_text_mode: "on_focus"
    required: True
    icon_right: "cellphone"
    icon_right_color: [1,1,1,1]
    pos_hint:{'center_x': 0.5, 'center_y': 0.5}
    size_hint_x:None
    width:250
"""
reason_input = """
MDTextField:
    hint_text: "Enter reason"
    helper_text: "Include some of the abusive messages"
    helper_text_mode: "on_focus"
    required: True
    multiline: True
    icon_right: "information"
    icon_right_color: [1,1,1,1]
    pos_hint:{'center_x': 0.5, 'center_y': 0.4}
    size_hint_x:None
    width:250
"""