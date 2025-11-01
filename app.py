#!/usr/bin/env python3
"""
FPL Optimizer Web Application
Flask-based web interface for the FPL Optimizer
"""
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider
import os
import traceback
import numpy as np
from fpl_api import FPLApi
from player_analyzer import PlayerAnalyzer
from team_optimizer import TeamOptimizer
from transfer_suggester import TransferSuggester
from captain_selector import CaptainSelector
from chip_advisor import ChipAdvisor


class NumpyJSONProvider(DefaultJSONProvider):
    """Custom JSON provider that handles numpy/pandas types"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


app = Flask(__name__)
app.json = NumpyJSONProvider(app)
app.secret_key = os.environ.get('SECRET_KEY', 'fpl-optimizer-secret-key-2024')
CORS(app)

# Global instances (initialized on first request)
api = None
analyzer = None
optimizer = None
transfer_suggester = None
captain_selector = None
chip_advisor = None


def convert_to_native_types(obj):
    """Recursively convert numpy/pandas types to native Python types"""
    if isinstance(obj, dict):
        return {key: convert_to_native_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_native_types(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, 'item'):  # For numpy scalars
        return obj.item()
    return obj


def initialize_components():
    """Initialize all FPL components"""
    global api, analyzer, optimizer, transfer_suggester, captain_selector, chip_advisor
    
    if api is None:
        api = FPLApi()
        analyzer = PlayerAnalyzer(api)
        analyzer.load_data()
        optimizer = TeamOptimizer(api, analyzer)
        transfer_suggester = TransferSuggester(api, analyzer, optimizer)
        captain_selector = CaptainSelector(api, analyzer)
        chip_advisor = ChipAdvisor(api, analyzer, transfer_suggester, captain_selector)


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page with team ID input"""
    team_id = request.args.get('team_id', '')
    return render_template('dashboard.html', team_id=team_id)


@app.route('/optimal-squad')
def optimal_squad_page():
    """Optimal squad builder page"""
    return render_template('optimal_squad.html')


@app.route('/value-players')
def value_players_page():
    """Value players page"""
    return render_template('value_players.html')


# API Routes
@app.route('/api/initialize', methods=['POST'])
def api_initialize():
    """Initialize the FPL data"""
    try:
        initialize_components()
        current_gw = api.get_current_gameweek()
        return jsonify({
            'success': True,
            'current_gameweek': current_gw,
            'message': 'Data loaded successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/optimal-squad', methods=['POST'])
def api_optimal_squad():
    """Get optimal squad selection"""
    try:
        initialize_components()
        data = request.get_json() or {}
        horizon = data.get('horizon', 5)
        budget = data.get('budget', 1000)
        
        result = optimizer.optimize_squad(budget=budget, horizon=horizon)
        result = convert_to_native_types(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/team-analysis/<int:team_id>', methods=['GET'])
def api_team_analysis(team_id):
    """Get comprehensive team analysis"""
    try:
        initialize_components()
        
        # Get current squad
        current_gw = api.get_current_gameweek()
        picks_data = api.get_team_picks(team_id, current_gw)
        current_squad = [pick['element'] for pick in picks_data['picks']]
        
        # Get all analyses
        lineup = optimizer.optimize_starting_xi(current_squad)
        transfers = transfer_suggester.suggest_transfers(team_id, num_transfers=1, horizon=5)
        captain = captain_selector.suggest_captain(current_squad)
        chips = chip_advisor.get_chip_recommendations(team_id)
        
        # Get team info
        team_info = api.get_team(team_id)
        
        # Convert all data to native types
        result = convert_to_native_types({
            'success': True,
            'team_info': {
                'name': team_info.get('name', 'Your Team'),
                'player_name': f"{team_info.get('player_first_name', '')} {team_info.get('player_last_name', '')}",
                'overall_points': team_info.get('summary_overall_points', 0),
                'overall_rank': team_info.get('summary_overall_rank', 0),
                'gameweek_points': team_info.get('summary_event_points', 0),
            },
            'lineup': lineup,
            'transfers': transfers,
            'captain': captain,
            'chips': chips,
            'current_gameweek': current_gw
        })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/transfers/<int:team_id>', methods=['POST'])
def api_transfers(team_id):
    """Get transfer suggestions"""
    try:
        initialize_components()
        data = request.get_json() or {}
        num_transfers = data.get('num_transfers', 1)
        horizon = data.get('horizon', 5)
        
        result = transfer_suggester.suggest_transfers(
            team_id, 
            num_transfers=num_transfers, 
            horizon=horizon
        )
        result = convert_to_native_types(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/captain/<int:team_id>', methods=['GET'])
def api_captain(team_id):
    """Get captain recommendations"""
    try:
        initialize_components()
        
        current_gw = api.get_current_gameweek()
        picks_data = api.get_team_picks(team_id, current_gw)
        current_squad = [pick['element'] for pick in picks_data['picks']]
        
        result = captain_selector.suggest_captain(current_squad)
        result = convert_to_native_types(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/chips/<int:team_id>', methods=['GET'])
def api_chips(team_id):
    """Get chip recommendations"""
    try:
        initialize_components()
        result = chip_advisor.get_chip_recommendations(team_id)
        result = convert_to_native_types(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/lineup/<int:team_id>', methods=['GET'])
def api_lineup(team_id):
    """Get optimal starting XI"""
    try:
        initialize_components()
        
        current_gw = api.get_current_gameweek()
        picks_data = api.get_team_picks(team_id, current_gw)
        current_squad = [pick['element'] for pick in picks_data['picks']]
        
        result = optimizer.optimize_starting_xi(current_squad)
        result = convert_to_native_types(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/value-players', methods=['GET'])
def api_value_players():
    """Get best value players"""
    try:
        initialize_components()
        
        position = request.args.get('position', type=int)
        limit = request.args.get('limit', 10, type=int)
        
        result = analyzer.get_value_players(position=position, limit=limit)
        
        # Convert DataFrame to dict and ensure native types
        players = result.to_dict('records')
        players = convert_to_native_types(players)
        
        return jsonify({
            'success': True,
            'players': players
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

