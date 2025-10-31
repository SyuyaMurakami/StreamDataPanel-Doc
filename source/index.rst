..
   Note: Items in this toctree form the top-level navigation. See `api.rst` for the `autosummary` directive, and for why `api.rst` isn't called directly.

.. toctree::
   :hidden:

   Home Page <self>
   modules.rst
   Install.rst
   Usage.rst
   Config.rst

Welcome to Use StreamDataPanel
================================

StreamDataPanel is a local-hosted web app, which is used to show frequently-freshed data as line chart, bar chart, pie chart, radar chart, scatter chart or surface chart. It is based on eel with python, optimized for speed.

Why Should I Use StreamDataPanel?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Most ploting libraries in python focus on static data. It could be difficult to show data which can be **freshed every second**. StreamDataPanel supplies a method to present it.

StreamDataPanel is designed to **asynchronously transmit data**. A chart can be subscribed with its data updated twice per second, while another chart can be updated 10 times per second. They won't influence each other. And you can open as many browser tabs as you want, or subscribe a same chart as many times as you want.

You can design your own data monitor panel with StreamDataPanel. Every chart in StreamDataPanel can be **dragged to resize or re-locate**. Your design can be saved into local disk, and re-upload to StreamDataPanel next time you want to use it.

StreamDataPanel provides a **user-friendly API**, making it easier to show your data. You do not need to worry about the form of axis tickers or axis value ranges, etc. All you need to do is to give a key word as title of a chart, and pass your data to API, fresh it any time you want.

StreamDataPanel **seperates web app with data server**. You can run your data updating process in one machine and subscribe these charts from others.

Who Can Use StreamDataPanel?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

StreamDataPanel is designed to show high-frequent data in a simple way. It is designed for derivative traders, student majoring in finance or anyone who is interested in high-frequent trading (HFT). Of course, it can be used outside finance area. It can convert any data into charts, and fresh them any time you want.

Important Notice
^^^^^^^^^^^^^^^^^^^^

To use the API of StreamDataPanel, you have to start it before using any class of it:
::

    from StreamDataPanel import *
    start_api()

Running without ``start_api`` will render an error. You may not be able to fresh your data.

If something went wrong, you can try to restart api by:
::

    restart_api()

**Important Notice**: No matter how many python scripts you run, **you can only start StreamDataPanel API in one of them**, because StreamDataPanel uses websockets in localhost to transmit data, starting more than once will lead to port conflict. If you have many different data streams to show, you should write a stand-alone script to summary these streams and interact with StreamDataPanel, rather than try to update them one by one in seperate python scripts.


Install
^^^^^^^^^^^^^

You can install StreamDataPanel as follows:
::

   pip install StreamDataPanel

Quick Test
^^^^^^^^^^^^^^^

To see functions of StreamDataPanel, you can simply run a test.

Use ``testSDP`` in terminal to run a test APP:
::

    testSDP

A web will be opened automatically. Type one of the following words below into ``ChartType`` input: 
::

    line
    bar
    sequence
    lines
    bars
    sequences
    pie
    radar
    scatter
    surface
    area
    areas
    text
    gauge

Then type ``test`` into ``KeyWord`` input. Click ``Subscribe`` to see if it runs correctly. If You see a chart with data freshed every second, it means success.

Quick Start
^^^^^^^^^^^^^^^

As mentioned above, the first thing is to import and start API:
::

    from StreamDataPanel import *
    start_api()

After it, you can choose a chart type and create an instance of it:
::

    line_chart = Line('this_is_a_title')

This title will be a key word when you try to subscribe this data, so **you can not have two charts which have the same chart-type and title**. It means you can not create two line charts, both have title named as ``this_is_a_title`` . However, you can create a line chart and a bar chart, both have the name ``this_is_a_title`` .

You can update data by ``fresh`` function:
::

    import time
    for i in range(10000):
        line_chart.fresh(i)
        time.sleep(0.25)

You should run this python script by:
::

    python your_script.py

Next step is to start a web app by the following command in **terminal**:
::

    runSDP

A web app should be started automatically, if everything is correct. Then type ``line`` into ``ChartType`` input, type ``this_is_a_title`` into ``KeyWord`` input. Click ``Subscribe`` to show your chart. You will see a line chart, which is a straight line updated 4 times per second.





