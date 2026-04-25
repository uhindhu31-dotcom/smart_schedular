from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# -------- Scheduling Algorithms -------- #

def fcfs(processes):
    processes.sort(key=lambda x: x['arrival'])
    time = 0
    waiting_time = 0

    for p in processes:
        if time < p['arrival']:
            time = p['arrival']
        waiting_time += time - p['arrival']
        time += p['burst']

    return waiting_time / len(processes)


def sjf(processes):
    processes.sort(key=lambda x: x['burst'])
    time = 0
    waiting_time = 0

    for p in processes:
        waiting_time += time
        time += p['burst']

    return waiting_time / len(processes)


def priority_scheduling(processes):
    processes.sort(key=lambda x: x['priority'])
    time = 0
    waiting_time = 0

    for p in processes:
        waiting_time += time
        time += p['burst']

    return waiting_time / len(processes)


def round_robin(processes, quantum=2):
    queue = processes.copy()
    time = 0
    waiting_time = 0

    remaining = {p['id']: p['burst'] for p in processes}

    while queue:
        p = queue.pop(0)
        if remaining[p['id']] > quantum:
            time += quantum
            remaining[p['id']] -= quantum
            queue.append(p)
        else:
            time += remaining[p['id']]
            waiting_time += time - p['burst']
            remaining[p['id']] = 0

    return waiting_time / len(processes)


# -------- API -------- #

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    processes = []
    for p in data:
        processes.append({
            'id': p['id'],
            'arrival': int(p['arrival']),
            'burst': int(p['burst']),
            'priority': int(p['priority'])
        })

    results = {
        "FCFS": fcfs(processes.copy()),
        "SJF": sjf(processes.copy()),
        "Priority": priority_scheduling(processes.copy()),
        "Round Robin": round_robin(processes.copy())
    }

    best_algo = min(results, key=results.get)

    return jsonify({
        "results": results,
        "best": best_algo
    })


if __name__ == '__main__':
    app.run(debug=True)