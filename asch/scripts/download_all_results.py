import json
from asch.server.participants import Participant

all_participants = Participant.fetch_all()
for f in all_participants:
    f.populate_task_data()

print(len(all_participants))

with open('output.json', 'w+') as ofile:
    ofile.write(json.dumps([Participant.todict(f, json_safe=True) for f in all_participants]))
