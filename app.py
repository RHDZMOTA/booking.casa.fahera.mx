import uuid
import datetime as dt

import streamlit as st

from rhdzmota.ext.streamlit_webapps.page_view import (
    PageViewHeader,
    PageView,
)
from rhdzmota.ext.streamlit_webapps import (
    PageViewSwitcher,
)


CASA_FAHERA_PROPS = [
    "anuva-suite",
    "demo"
]

CASA_FAHERA_DEFAULT_PROP = "anuva-suite"

def session_info_get_or_create() -> {}:
    # Do we have a current session key in local storage?
    sess_key = st.session_state.get("current_sess_key")
    if sess_key:
        session_info = st.session_state.get(sess_key) or {}
        st.query_params.sess_key = sess_key
        st.session_state[sess_key] = session_info
        return session_info
    # Can we get the session key from the query params?
    if "sess_key" in (params := st.query_params.to_dict()):
        sess_key = params["sess_key"]
        st.session_state["current_sess_key"] = sess_key
        return session_info_get_or_create()
    # Create new session key
    sess_key = str(uuid.uuid4())
    st.query_params.sess_key = sess_key
    st.session_state["current_sess_key"] = sess_key
    return session_info_get_or_create()


class BookingHeader(PageViewHeader):
    def on_start(self):
        session_info = session_info_get_or_create()
        if "preselect" not in st.query_params.to_dict():
            st.query_params.preselect = "anuva-suite"
        st.markdown(f"# Casa Fahera Booking")


class Landing(PageView, BookingHeader):
    
    def view(self, **kwargs):

        prop_preselect = st.query_params.preselect
        with st.form(key="casa-fahera-form-prop"):
            property_key = st.selectbox(
                "Casa Fahera Property",
                CASA_FAHERA_PROPS,
                index=CASA_FAHERA_PROPS.index(prop_preselect),

            )
            email = st.text_input(label="Email")
            submitted = st.form_submit_button()

        if not submitted:
            return
        if "@" not in email:
            return st.error(f"Invalid email: {email}")


class Booking(PageView, BookingHeader):
    def view(self, **kwargs):
        x = st.date_input(
            "Select your stay",
            value=(today := dt.datetime.today()),
            min_value=today,
            max_value=dt.date(today.year + 4, 1, 1),
            format="YYYY-MM-DD",
        )


if __name__ == "__main__":
    landing = Landing(page_layout="centered")
    booking = Booking(page_layout="centered")
    switcher = PageViewSwitcher.from_page_views(
        switcher_name="CFB",
        page_views=[landing, booking],
    )
    switcher.run(initial_page_key=booking.refname)
