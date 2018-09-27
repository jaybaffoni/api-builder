var express = require('express');
var router = express.Router();
var mysql = require('mysql');
var mc = mysql.createConnection({
	host: '127.0.0.1',
	user: 'root',
	password: 'theenemysgateisdown',
	database: 'example',
});

mc.connect();

// Retrieve all
router.get('/', function(req, res) {

	mc.query('SELECT * FROM objects', function (error, results, fields) {
		if( error) throw error;
		res.send(results);
	});
});



// Retrieve by first column
router.get('/:id', function(req, res) {
	let id = req.params.id;

	mc.query('SELECT * FROM objects WHERE object_id=?', id, function (error, results, fields) {
		if( error) throw error;
		res.send(results);
	});
});



// Delete by first column
router.delete('/:id', function(req, res) {
	let id = req.params.id;

	mc.query('DELETE FROM objects WHERE object_id=?', id, function (error, results, fields) {
		if( error) throw error;
		res.send(results);
	});
});

// Create
router.post('/', function(req, res) {
	let object_id = req.body.data.object_id;
	let data = req.body.data.data;
	let info = req.body.data.info;
	let details = req.body.data.details;

	mc.query('INSERT INTO objects SET?', {object_id: object_id, data: data, info: info, details: details, }, function (error, results, fields) {
		if( error) throw error;
		res.send(results);
	});
});

// Update
router.put('/', function(req, res) {
	let object_id = req.body.data.object_id;
	let data = req.body.data.data;
	let info = req.body.data.info;
	let details = req.body.data.details;

	mc.query('UPDATE objects SET ? WHERE object_id=?', [{data: data, info: info, details: details, }, object_id], function (error, results, fields) {
		if( error) throw error;
		res.send(results);
	});
});



module.exports = router;