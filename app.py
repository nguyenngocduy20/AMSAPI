from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)
todos = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': 'refactor an API'},
    'todo3': {'task': 'rebuild an API'}
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in todos:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('task')


class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return todos[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        todos[todo_id] = task
        return task, 201


class TodoList(Resource):
    def get(self):
        return todos

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(todos.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        todos[todo_id] = {'task': args['task']}
        return todos[todo_id], 201

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


api.add_resource(TodoList, '/todos');
api.add_resource(Todo, '/todos/<todo_id>')
if __name__ == '__main__':
    app.run(debug=True)
