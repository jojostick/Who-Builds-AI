"""Headless Streamlit interaction checks; not a browser layout inspection."""
from streamlit.testing.v1 import AppTest

def check(app):
    assert not app.exception, [e.message for e in app.exception]

app = AppTest.from_file('app.py', default_timeout=30).run()
check(app)
assert app.metric[0].value == '867'
assert app.metric[2].value == '96.9%'
app.checkbox[0].check().run()
check(app)
app.checkbox[0].uncheck().run()
app.slider[0].set_value((2024,2025)).run()
check(app)
app.selectbox[0].select(2024).run()
check(app)
app.multiselect[0].set_value([]).run()
check(app)
app.slider[0].set_value((2010,2010)).run()
check(app)
print('PASS: default render, sensitivity toggle, year range, verification year, empty country selection, single-year range')
