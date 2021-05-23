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
    debug = 0
    cur = con.cursor()

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

    data = pd.read_sql(sql, con)
    log = data;
    ege = data.pop('ege')
    participants = data.pop('ParticipantId')
    subjects = data.pop('SubjectId')
    data = data.replace(np.nan, 0)

    print(data.head())
    print(ege.head())
    print(participants.head())

    dataset = tf.data.Dataset.from_tensor_slices((data.values, ege.values))
    for feat, targ in dataset.take(10):
        print('Features: {}, Target: {}'.format(feat, targ))

    train_x = data
    train_y = ege


    def get_compiled_model():
        model = keras.Sequential([
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(1024, activation='relu'),
            keras.layers.Dense(1)
        ])

        model.compile(optimizer='adam',
                      loss='mse',
                      metrics=keras.metrics.RootMeanSquaredError())

        return model



    model = tf.keras.models.load_model('my_model')
    if(debug):
        model = get_compiled_model()
        model.fit(train_x, train_y, epochs=100)

    model.save('my_model')

    pred = model.predict(train_x)

    for i in pred:
        i[0] *= 100


    print(pred[0][0], train_y[0] * 100)
    print(pred[1][0], train_y[1] * 100)
    print(pred[2][0], train_y[2] * 100)
    print(pred[3][0], train_y[3] * 100)
    print(pred[4][0], train_y[4] * 100)
    print(pred[5][0], train_y[5] * 100)
    print(pred[6][0], train_y[6] * 100)
    print(pred[7][0], train_y[7] * 100)
    print(pred[8][0], train_y[8] * 100)
    print(pred[9][0], train_y[9] * 100)

    l = data.join(participants)
    l = l.join(subjects)
    l = l.join(pd.DataFrame(pred))
    l.pop('dr')
    l.pop('sdr')

    print(l.head())

    l.to_csv("submission.csv", sep=';')



