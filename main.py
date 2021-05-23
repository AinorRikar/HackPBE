import pymysql
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras


con = pymysql.connect(host='localhost',
                      user='root',
                      password='password1234',
                      db='hackathon',
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)

with con:
    debug = 1
    cur = con.cursor()
    cur.execute("SELECT * FROM egeresults;")
    ege = cur.fetchall()
    cur.execute("SELECT * FROM selfdiagnosticresults;")
    self_diagnostic = cur.fetchall()
    cur.execute("SELECT * FROM diagnosticresults;")
    diagnostic = cur.fetchall()
    try:
        for i in range(len(ege)):
            q = ege[i]["SubjectId"]
            if q != 4 or q != 9 or q != 27 or q != 61 or q != 61 or q != 75 or q != 77 or q != 86 or q != 49:
                ege.pop(i)
    except:
        pass

    try:
        for i in range(len(self_diagnostic)):
            q = self_diagnostic[i]["SubjectId"]
            if q != 4 or q != 5 or q != 6 or q != 27 or q != 9 or q != 51 or q != 63 or q != 24 or q != 25 or q != 26 or q != 27 or q != 28 or q != 39 or q != 40 or q != 61 or q != 66 or q != 44 or q != 75 or q != 77 or q != 7 or q != 13 or q != 3 or q != 51 or q != 86:
                self_diagnostic.pop(i)
    except:
        pass

    try:
        for i in range(len(diagnostic)):
            q = diagnostic[i]["SubjectId"]
            if q != 4 or q != 5 or q != 6 or q != 27 or q != 9 or q != 51 or q != 63 or q != 24 or q != 25 or q != 26 or q != 27 or q != 28 or q != 39 or q != 40 or q != 61 or q != 66 or q != 44 or q != 75 or q != 77 or q != 7 or q != 13 or q != 3 or q != 51 or q != 86:
                diagnostic.pop(i)
    except:
        pass

    print(len(ege))
    print(len(self_diagnostic))
    print(len(diagnostic))

    ege_list = []
    ege_list1 = []
    for i in range(len(ege)):
        for vaiue in ege[i].values():
            ege_list1.append(vaiue)
        ege_list.append(ege_list1)
        ege_list1 = []

    self_diagnostic_list = []
    self_diagnostic_list1 = []
    for i in range(len(self_diagnostic)):
        for vaiue in self_diagnostic[i].values():
            self_diagnostic_list1.append(vaiue)
        self_diagnostic_list.append(self_diagnostic_list1)
        self_diagnostic_list1 = []

    diagnostic_list = []
    diagnostic_list1 = []
    for i in range(len(diagnostic)):
        for vaiue in diagnostic[i].values():
            diagnostic_list1.append(vaiue)
        diagnostic_list.append(diagnostic_list1)
        diagnostic_list1 = []

    # print(ege_list[1])

    for i in range(len(ege_list)):
        ege_list[i].pop(0)
        ege_list[i].pop(1)
        ege_list[i].pop(-1)

    for i in range(len(diagnostic_list)):
        diagnostic_list[i].pop(0)
        diagnostic_list[i].pop(0)
        diagnostic_list[i].pop(1)
        diagnostic_list[i].pop(1)
        diagnostic_list[i].pop(-1)

    for i in range(len(self_diagnostic_list)):
        self_diagnostic_list[i].pop(0)
        self_diagnostic_list[i].pop(1)
        self_diagnostic_list[i].pop(1)
        self_diagnostic_list[i].pop(-1)
        pass

    result1 = []
    dr1 = 0
    ndr = 0
    sdr = 0
    nsdr = 0

    for i in range(len(self_diagnostic_list)):
        if self_diagnostic_list[i][2] == None:
            self_diagnostic_list[i][2] = 0
        if self_diagnostic_list[i][1] == None:
            self_diagnostic_list[i][1] = 0

    for i in range(len(diagnostic_list)):
        if diagnostic_list[i][2] == None:
            diagnostic_list[i][2] = 0
        if diagnostic_list[i][1] == None:
            diagnostic_list[i][1] = 0
    result = pd.DataFrame(columns=['stud', 'les', 'DR', 'SDR', 'EGE'])
    for i in range(len(ege_list)):
        dr = 0
        sdr = 0
        dr1 = 0
        ndr = 0
        sdr = 0
        nsdr = 0
        stud = ege_list[i][0]
        les = ege_list[i][2]
        if les == 4:
            for j in range(len(diagnostic_list)):
                if stud in diagnostic_list[j]:
                    if diagnostic_list[j][3] == 4 or diagnostic_list[j][3] == 5 or diagnostic_list[j][3] == 6 or \
                            diagnostic_list[j][3] == 38:
                        dr1 = dr1 + (diagnostic_list[j][1] / diagnostic_list[j][2])
                        ndr = ndr + 1
            if ndr != 0:
                dr = dr1 / ndr
            dr1 = 0
            ndr = 0

            for j in range(len(self_diagnostic_list)):
                if stud in self_diagnostic_list[j]:
                    if self_diagnostic_list[j][3] == 4 or self_diagnostic_list[j][3] == 5 or self_diagnostic_list[j][
                        3] == 6 or self_diagnostic_list[j][3] == 38:
                        sdr1 = sdr1 + (self_diagnostic_list[j][1] / self_diagnostic_list[j][2])
                        nsdr = nsdr + 1
            if sdr != 0:
                sdr = sdr1 / ndr
            sdr1 = 0
            nsdr = 0
        elif les == 9:
            for j in range(len(diagnostic_list)):
                if stud in diagnostic_list[j]:
                    if diagnostic_list[j][3] == 9 or diagnostic_list[j][3] == 51 or diagnostic_list[j][3] == 63:
                        dr1 = dr1 + (diagnostic_list[j][1] / diagnostic_list[j][2])
                        ndr = ndr + 1
            if ndr != 0:
                dr = dr1 / ndr

            dr1 = 0
            ndr = 0

            for j in range(len(self_diagnostic_list)):
                if stud in self_diagnostic_list[j]:
                    if self_diagnostic_list[j][3] == 9 or self_diagnostic_list[j][3] == 51 or self_diagnostic_list[j][
                        3] == 63:
                        sdr1 = sdr1 + (self_diagnostic_list[j][1] / self_diagnostic_list[j][2])
                        nsdr = nsdr + 1
            if sdr != 0:
                sdr = sdr1 / ndr
            sdr1 = 0
            nsdr = 0
        elif les == 27:
            for j in range(len(diagnostic_list)):
                if stud in diagnostic_list[j]:
                    if diagnostic_list[j][3] == 24 or diagnostic_list[j][3] == 26 or diagnostic_list[j][3] == 25 or \
                            diagnostic_list[j][3] == 27 or diagnostic_list[j][3] == 28 or diagnostic_list[j][3] == 39 or \
                            diagnostic_list[j][3] == 40:
                        dr1 = dr1 + (diagnostic_list[j][1] / diagnostic_list[j][2])
                        ndr = ndr + 1
            if ndr != 0:
                dr = dr1 / ndr
            dr1 = 0
            ndr = 0

            for j in range(len(self_diagnostic_list)):
                if stud in self_diagnostic_list[j]:
                    if self_diagnostic_list[j][3] == 24 or self_diagnostic_list[j][3] == 26 or self_diagnostic_list[j][
                        3] == 25 or self_diagnostic_list[j][3] == 27 or self_diagnostic_list[j][3] == 28 or \
                            self_diagnostic_list[j][3] == 39 or self_diagnostic_list[j][3] == 40:
                        sdr1 = sdr1 + (self_diagnostic_list[j][1] / self_diagnostic_list[j][2])
                        nsdr = nsdr + 1
            if sdr != 0:
                sdr = sdr1 / ndr
            sdr1 = 0
            nsdr = 0
        elif les == 61:
            for j in range(len(diagnostic_list)):
                if stud in diagnostic_list[j]:
                    if diagnostic_list[j][3] == 61 or diagnostic_list[j][3] == 66:
                        dr1 = dr1 + (diagnostic_list[j][1] / diagnostic_list[j][2])
                        ndr = ndr + 1
            if ndr != 0:
                dr = dr1 / ndr
            dr1 = 0
            ndr = 0

            for j in range(len(self_diagnostic_list)):
                if stud in self_diagnostic_list[j]:
                    if self_diagnostic_list[j][3] == 61 or self_diagnostic_list[j][3] == 66:
                        sdr1 = sdr1 + (self_diagnostic_list[j][1] / self_diagnostic_list[j][2])
                        nsdr = nsdr + 1
            if sdr != 0:
                sdr = sdr1 / ndr
            sdr1 = 0
            nsdr = 0
        elif les == 75:
            for j in range(len(diagnostic_list)):
                if stud in diagnostic_list[j]:
                    if diagnostic_list[j][3] == 44 or diagnostic_list[j][3] == 75:
                        dr1 = dr1 + (diagnostic_list[j][1] / diagnostic_list[j][2])
                        ndr = ndr + 1
            if ndr != 0:
                dr = dr1 / ndr
            dr1 = 0
            ndr = 0

            for j in range(len(self_diagnostic_list)):
                if stud in self_diagnostic_list[j]:
                    if self_diagnostic_list[j][3] == 44 or self_diagnostic_list[j][3] == 75:
                        sdr1 = sdr1 + (self_diagnostic_list[j][1] / self_diagnostic_list[j][2])
                        nsdr = nsdr + 1
            if sdr != 0:
                sdr = sdr1 / ndr
            sdr1 = 0
            nsdr = 0
        elif les == 77:
            for j in range(len(diagnostic_list)):
                if stud in diagnostic_list[j]:
                    if diagnostic_list[j][3] == 77 or diagnostic_list[j][3] == 7 or diagnostic_list[j][3] == 13 or \
                            diagnostic_list[j][3] == 3:
                        dr1 = dr1 + (diagnostic_list[j][1] / diagnostic_list[j][2])
                        ndr = ndr + 1
            if ndr != 0:
                dr = dr1 / ndr
            dr1 = 0
            ndr = 0
            for j in range(len(self_diagnostic_list)):
                if stud in self_diagnostic_list[j]:
                    if self_diagnostic_list[j][3] == 77 or self_diagnostic_list[j][3] == 7 or self_diagnostic_list[j][
                        3] == 13 or self_diagnostic_list[j][3] == 3:
                        sdr1 = sdr1 + (self_diagnostic_list[j][1] / self_diagnostic_list[j][2])
                        nsdr = nsdr + 1
            if sdr != 0:
                sdr = sdr1 / ndr
            sdr1 = 0
            nsdr = 0
        elif les == 86:
            for j in range(len(diagnostic_list)):
                if stud in diagnostic_list[j]:
                    if diagnostic_list[j][3] == 51 or diagnostic_list[j][3] == 86:
                        dr1 = dr1 + (diagnostic_list[j][1] / diagnostic_list[j][2])
                        ndr = ndr + 1
            if ndr != 0:
                dr = dr1 / ndr
            dr1 = 0
            ndr = 0

            for j in range(len(self_diagnostic_list)):
                if stud in self_diagnostic_list[j]:
                    if self_diagnostic_list[j][3] == 51 or self_diagnostic_list[j][3] == 86:
                        sdr1 = sdr1 + (self_diagnostic_list[j][1] / self_diagnostic_list[j][2])
                        nsdr = nsdr + 1
            if sdr != 0:
                sdr = sdr1 / ndr
            sdr1 = 0
            nsdr = 0
        result.loc[len(result)] = [stud, les, dr, sdr, ege_list[i][1]]

    dfq = result.query("DR==0 and SDR==0")
    # print(dfq)
    res = result[~result.index.isin(dfq.index)]
    print(res)

    sql = """SELECT egeresults.ParticipantId, egeresults.SubjectId,
    egeresults.MarkPercent / 100 "ege",
    diagnosticresults.Mark / diagnosticresults.MaxMark "dr",
    selfdiagnosticresults.Mark / selfdiagnosticresults.MaxMark "sdr"
FROM egeresults
INNER JOIN subjects ON subjects.Id = egeresults.SubjectId
LEFT JOIN diagnosticresults ON (egeresults.SubjectId, egeresults.ParticipantId) = (diagnosticresults.SubjectId, diagnosticresults.ParticipantId)
LEFT JOIN selfdiagnosticresults ON (egeresults.SubjectId, egeresults.ParticipantId) = (selfdiagnosticresults.SubjectId, selfdiagnosticresults.ParticipantId)
WHERE ((egeresults.SubjectId, egeresults.ParticipantId)
		IN (SELECT SubjectId, ParticipantId FROM diagnosticresults)
	OR (egeresults.SubjectId, egeresults.ParticipantId)
		IN (SELECT SubjectId, ParticipantId FROM selfdiagnosticresults))
	AND egeresults.SubjectId = 75"""
    log = res
    participants = res.pop('stud')
    ege = res.pop('EGE')
    subjects = res.pop('les')
    data = res


    print(data.head())
    print(ege.head())
    print(participants.head())

    data = np.asarray(data).astype('float32')
    ege = np.asarray(ege).astype('float32')

    train_x = pd.DataFrame(data)
    train_y = ege


    def get_compiled_model():
        model = keras.Sequential([
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dense(512, activation='sigmoid'),
            keras.layers.Dense(1024, activation='relu'),
            keras.layers.Dense(256, activation='sigmoid'),
            keras.layers.Dense(1)
        ])

        model.compile(optimizer='adamax',
                      loss='mae',
                      metrics=keras.metrics.RootMeanSquaredError())

        return model



    print(len(train_x))
    print(len(train_y))

    model = tf.keras.models.load_model('my_model')
    if(debug > 0):
        model = get_compiled_model()
        model.fit(train_x, train_y, epochs=100)

    model.save('my_model')

    pred = model.predict(train_x)

    print(pred[0][0], train_y[0])
    print(pred[1][0], train_y[1])
    print(pred[2][0], train_y[2])
    print(pred[3][0], train_y[3])
    print(pred[4][0], train_y[4])
    print(pred[5][0], train_y[5])
    print(pred[6][0], train_y[6])
    print(pred[7][0], train_y[7])
    print(pred[8][0], train_y[8])
    print(pred[9][0], train_y[9])

    l = pd.DataFrame(data).join(participants)
    l = l.join(subjects)
    l = l.join(pd.DataFrame(pred))
    l.pop('DR')
    l.pop('SDR')

    print(l.head())

    l.to_csv("submission.csv", sep=';')



