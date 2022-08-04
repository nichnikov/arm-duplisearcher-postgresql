import os
import json
from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from utils import Worker
from uuid import uuid4
from waitress import serve
import logging


def data_prepare(json_data):
    """преобразует входящие словари в список кортежей"""
    queries_in = []
    for d in json_data:
        queries_in += [(d["locale"], d["moduleId"], str(uuid4()),
                        d["id"], tx, d["pubIds"]) for tx in d["clusters"]]
    return queries_in


logger = logging.getLogger("app_duplisearcher")
logger.setLevel(logging.INFO)


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)

name_space = api.namespace('api', 'На вход поступает JSON, возвращает JSON')

query = name_space.model("One Query",
                         {"id": fields.String(description="query's Id", required=True),
                          "cluster": fields.String(description="query's text", required=True)})

input_data = name_space.model("Input JSONs",
                              {"score": fields.Float(description="The similarity coefficient", required=True),
                               "data": fields.List(fields.Nested(query)),
                               "operation": fields.String(description="add/update/delete/search/del_all",
                                                          required=True)})


with open(os.path.join("data", "config.json")) as json_config_file:
    config = json.load(json_config_file)

print("config:", config)

main = Worker(config["shard_size"], config["dictionary_size"])


@name_space.route('/')
class CollectionHandling(Resource):
    """Service searches duplicates and adding and delete data in collection."""

    @name_space.expect(input_data)
    def post(self):
        """POST method on input JSON file with scores, operation type and lists of fast answers."""
        json_data = request.json

        if json_data["data"]:
            queries = data_prepare(json_data["data"])
            lc, m_i, q_i, a_i, txs, p_ids = zip(*queries)
            if json_data["operation"] == "add":
                main.add(queries)
                logger.info("quantity:" + str([len(m.ids) for m in main.matrix_list.ids_matrix_list]))
                return jsonify({"quantity": sum([len(m.ids) for m in main.matrix_list.ids_matrix_list])})

            elif json_data["operation"] == "delete":
                main.delete(list(set(q_i)))
                logger.info("quantity:" + str([len(m.ids) for m in main.matrix_list.ids_matrix_list]))
                return jsonify({"quantity": sum([len(m.ids) for m in main.matrix_list.ids_matrix_list])})

            elif json_data["operation"] == "update":
                main.update(queries)
                logger.info("data were updated")
                return jsonify({"quantity": sum([len(m.ids) for m in main.matrix_list.ids_matrix_list])})

            elif json_data["operation"] == "search":
                try:
                    if "score" in json_data:
                        search_results = main.search(queries, json_data["score"])
                    else:
                        search_results = main.search(queries)
                    return jsonify(search_results)
                except:
                    return jsonify([])
        else:
            if json_data["operation"] == "delete_all":
                main.delete_all()
                logger.info("quantity:" + str([len(m.ids) for m in main.matrix_list.ids_matrix_list]))
                return jsonify({"quantity": sum([len(m.ids) for m in main.matrix_list.ids_matrix_list])})


if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=8080)
    app.run(host='0.0.0.0', port=8080)
