const Team = require('../models/Team');

class TeamService {
  async createTeam(teamData) {
    const team = new Team(teamData);
    return await team.save();
  }

  async getTeamById(id) {
    return await Team.findById(id).populate('agency members lead', 'name email firstName lastName');
  }

  async getTeamsByAgency(agencyId) {
    return await Team.find({ agency: agencyId }).populate('agency members lead', 'name email firstName lastName');
  }

  async updateTeam(id, updateData) {
    return await Team.findByIdAndUpdate(id, updateData, { new: true, runValidators: true });
  }

  async deleteTeam(id) {
    return await Team.findByIdAndDelete(id);
  }
}

module.exports = new TeamService();