import pandas as pd
import json
from fpdf import FPDF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

test_case_related_info = [['Name', 'Start Time', 'Step', 'Uri', 'End Time']]
feature_related_info = [['Description', 'Name', 'Type', 'Uri']]
scenerio_related_info = [['Scenario No', 'Name', 'Start Time', 'Type', 'Uri', 'Stop Time']]
steps_related_info = [['Step No', 'Name', 'Start Time', 'Stop Time', 'Comparision Detail', 'Result']]


xxx = ['Name', 'Start Time', 'Step', 'Uri', 'End Time']
overall_test_related_info = []
total_number_of_test = 0

with open('results.json', 'r') as f:
    data = json.loads(f.read())
# d1 = data["tests"][0]
suite_related_data = data["tests"][0]
suite_name = suite_related_data["name"]
suite_start_time = suite_related_data["start"]
suite_type = suite_related_data["type"]
suite_uri = suite_related_data["uri"]
suite_end_time = suite_related_data["stop"]

# print(suite_name, "---", suite_start_time, "---", )

test_related_data = suite_related_data["tests"]
# print(test_related_data)
for test in test_related_data:
    feature_related_data = test["tests"][0]
    scenerio_related_data = feature_related_data["tests"]

    test_case_related_info.append([test["name"], test["start"], test["type"], test["uri"], test["stop"]])
    feature_related_info.append([feature_related_data['description'], feature_related_data['name'],
                                 feature_related_data["type"], feature_related_data["uri"]])

    scenerio_counter = 0
    for scenerio in scenerio_related_data:
        scenerio_related_info.append([scenerio_counter + 1, scenerio['name'], scenerio['start'], scenerio['type'],
                                      scenerio['uri'], scenerio['stop']])
        scenerio_counter += 1
        steps_related_data = scenerio["tests"]
        step_counter = 0
        for steps in steps_related_data:
            comparision_data = steps["tests"]

            for i in range(len(comparision_data)):
                comparision_data = comparision_data[i]

            if len(comparision_data) != 0:
                steps_related_info.append([step_counter + 1, steps['name'], steps['start'],
                                           steps['stop'], comparision_data['detail'],
                                           comparision_data['result']])
            else:
                steps_related_info.append([step_counter + 1, steps['name'], steps['start'], steps['stop'],
                                           'NA', 'NA'])
            step_counter += 1



# print(test_case_related_info)
# print(feature_related_info)
# print(scenerio_related_info)
# print(steps_related_info)
# for i in steps_related_info:
#     print(i)

print(steps_related_info)
# df = pd.DataFrame()
# step_df = pd.DataFrame(steps_related_info, columns=xxx)
# print(step_df.head())
# print(df.columns)
# print(df.iloc[0])


pdf = FPDF()
pdf.alias_nb_pages()
epw = pdf.w - 2*pdf.l_margin
test_col_width = epw/5
feature_col_width = epw/4
scenario_col_width = epw/6
steps_col_width = epw/6
pdf.set_line_width(0.5)

pdf.add_page()

# Save top coordinate
# top = pdf.y + 20

# Calculate x position of next cell
# offset = pdf.x + col_width

pdf.set_font('Times', 'B', 20)
pdf.set_draw_color(128, 128, 128)
pdf.set_fill_color(211, 211, 211)

# to add page border
pdf.line(5.0, 5.0, 205.0, 5.0)
pdf.line(5.0, 292.0, 205.0, 292.0)
pdf.line(5.0, 5.0, 5.0, 292.0)
pdf.line(205.0, 5.0, 205.0, 292.0)

# suite_name = "Auto_Deliver_SAPCEC_101_4567"
pdf.cell(epw, 15, suite_name, 1, 1, 'C', fill=1)
pdf.ln(10)

# test case heading
pdf.set_font('Times', '', 12)
pdf.cell(0, 7, 'Test Related Info-', 1, 1, 'L', fill=1)
pdf.ln(5)


# for first table
pdf.set_font('Times', '', 12)
pdf.set_draw_color(128, 128, 128)

th = pdf.font_size

for row in test_case_related_info:
    # print(ybefore, '---', xbefore)
    for datum in row:
        # Enter data in columns
        # Notice the use of the function str to coerce any input to the
        # string type. This is needed
        # since pyFPDF expects a string, not a number.
        # pdf.cell(col_width, 1.5 * th, str(row), border=1)
        ybefore = pdf.get_y()
        xbefore = pdf.get_x()
        pdf.multi_cell(test_col_width, 2*th, str(datum), align='C', border=0, fill=1)
        pdf.set_xy(test_col_width + xbefore, ybefore)
    pdf.ln(2*th)

pdf.ln(25)

# feature case heading
pdf.set_font('Times', '', 12)
pdf.cell(0, 7, 'Feature Related Info-', 1, 1, 'L', fill=1)
pdf.ln(5)

for row in feature_related_info:
    # print(ybefore, '---', xbefore)
    for datum in row:
        # Enter data in columns
        # Notice the use of the function str to coerce any input to the
        # string type. This is needed
        # since pyFPDF expects a string, not a number.
        # pdf.cell(col_width, 1.5 * th, str(row), border=1)
        ybefore = pdf.get_y()
        xbefore = pdf.get_x()
        pdf.multi_cell(feature_col_width, 2*th, str(datum), align='C', border=0, fill=1)
        pdf.set_xy(feature_col_width + xbefore, ybefore)
    pdf.ln(2*th)


pdf.ln(25)

# scenario case heading
pdf.set_font('Times', '', 12)
pdf.cell(0, 7, 'Scenario Related Info-', 1, 1, 'L', fill=1)
pdf.ln(5)

diff_arr = []
# height test
for row in scenerio_related_info:
    # print(ybefore, '---', xbefore)
    for datum in row:
        str_width = pdf.get_string_width(str(datum))

        if str_width > scenario_col_width:
            diff = str_width - scenario_col_width
            diff_arr.append(diff)
max_diff = max(diff_arr)
print(diff_arr, max_diff)
# h_per = (scenario_col_width * 100) % str_width
# height = ((2*th) * h_per) % 100
# print(height)
height = (2*th) * 2

for row in scenerio_related_info:
    # print(ybefore, '---', xbefore)
    for datum in row:
        # Enter data in columns
        # Notice the use of the function str to coerce any input to the
        # string type. This is needed
        # since pyFPDF expects a string, not a number.
        # pdf.cell(col_width, 1.5 * th, str(row), border=1)
        # nlines = len(pdf.Split)
        ybefore = pdf.get_y()
        xbefore = pdf.get_x()
        pdf.cell(20, 2*th, str(datum), align='C', border=1, fill=1)
        pdf.set_xy(20 + xbefore, ybefore)
    pdf.ln(2*th)

# pdf.ln(20)
# # steps case heading
# pdf.set_font('Times', '', 12)
# pdf.cell(0, 7, 'Steps Related Info-', 1, 1, 'L', fill=1)
# pdf.ln(5)
#
# for row in steps_related_info:
#     # print(ybefore, '---', xbefore)
#     for datum in row:
#         # Enter data in columns
#         # Notice the use of the function str to coerce any input to the
#         # string type. This is needed
#         # since pyFPDF expects a string, not a number.
#         # pdf.cell(col_width, 1.5 * th, str(row), border=1)
#         ybefore = pdf.get_y()
#         xbefore = pdf.get_x()
#         pdf.multi_cell(steps_col_width, 2*th, str(datum), align='C', border=1, fill=1)
#         pdf.set_xy(steps_col_width + xbefore, ybefore)
#     pdf.ln(2*th)

pdf.output('first_report.pdf', 'F')



## MAtplotlib trail
# fig, ax = plt.subplots(1, figsize=(10,10))
# ax.axis('tight')
# ax.axis('off')
# x = ax.table(cellText=test_case_related_info, colLabels=xxx, loc="center", colLoc='center')
# x.scale(1.5, 1.5)
#
# pdf = PdfPages('first_report.pdf')
# pdf.savefig(fig)
# pdf.close()
# plt.show()
















































#
#
# with open('results.json','r') as f:
#     data = json.loads(f.read())
# d1 = data["tests"][0]
# print(d1)
# d2 = d1["tests"][0]
# print(d2)
# d3 = d2["tests"][0]
# multiple_level_data = pd.json_normalize(d3, record_path=['tests'],
#                                         meta=['name', 'start', 'type', 'uri', ],
#                                         meta_prefix='config_params_', record_prefix='test_')
# multiple_level_data.to_html('multiplelevel_normalized_data3.html', index=False)
# print(multiple_level_data)
# d1 = data["tests"]
# # print(d1)
# df = pd.DataFrame(data=data["tests"])
# df = df.fillna(' ').T
# # print(df.to_html())
# json_data = json.dumps(data)
# print(type(json_data))
# t_data = data["tests"][0]
# suite related data
# #
# # print(t_data)
# # print("***********************************************************************************")
# # t1_data = t_data["tests"][0]
# # print(t1_data)
# # print("*********************************************************************************")
# # t2_data = t1_data["tests"][0]
# # print(t2_data)
# # print("**********************************************************************************")
# # # steps related data
# # t3_data = t2_data["tests"][0]
# # t3_data_arr = t2_data["tests"]
# # for i in range(len(t3_data_arr)):
# #     scenerio_name = t3_data_arr[i]["name"]
# #     print(scenerio_name)
# # print(t3_data)
#
# # print(len(t3_data_arr))
# # print("**********************************************************************************")
# # t4_data = t3_data["tests"]
# # print(t4_data)
# # print(len(t4_data))
# # # print(t1_data["description"])


# import codecs
# import json
# from json2html import *
# import pandas as pd
# with open("results.json", 'r') as f:
#     data = json.load(f)
# d1 = data["tests"][0]
# d2 = d1["tests"][0]
# d3 = d2["tests"][0]
# json_data = json.dumps(d3)
# html_syn = json2html.convert(json=json_data)
# content = ''
# with open("multiplelevel_normalized_data1.html", 'w') as r:
#     r.write(html_syn)
# with open("multiplelevel_normalized_data1.html", 'r') as d:
#     content += d.read()
#
# table_list = content.split('<tr>')
# for i in table_list:
#     print(i)
# print(len(table_list))
# print(table_list)
# print(content)
# f=codecs.open("multiplelevel_normalized_data1.html", 'r')
# data = f.read()
# print(data)
# list_data = data.split("<table")
# print(list_data)