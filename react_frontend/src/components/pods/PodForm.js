import React, {PropTypes} from 'react';
import TextInput from '../common/TextInput';
import Select from '../common/Select';

class PodForm extends React.Component {
  constructor(props) {
    super(props);
    this.makePlayerInputs = this.makePlayerInputs.bind(this);
  }

  makePlayerInputs() {
    return this.props.pod.players.map((player, index) => {
      return (
        <div className="row" key={index}>
          <div className="col-xs-6">
            <TextInput
              name="email"
              label={index == 0 ? "Your Email" : "Player " + index + " Email"}
              onChange={this.props.onPlayerChange}
              customValue={index.toString()}
            />
          </div>
          <div className="col-xs-6">
            <TextInput
              name="name"
              label={index == 0 ? "Your Name" : "Player " + index + " Name"}
              onChange={this.props.onPlayerChange}
              customValue={index.toString()}
            />
          </div>
        </div>
      );
    });
  }

  render() {
    const players = this.makePlayerInputs();
    return (
      <div>
        <form>
          <TextInput
            name="name"
            label="Pod Name"
            value={this.props.pod.name}
            onChange={this.props.onChange}/>

          <Select
            name="pack_1_set"
            label="First Pack Set"
            value={this.props.pod.pack_1_set}
            options={this.props.sets.map(function(set) {return {value: set.code, display: set.name, selected: false}} )}
            onChange={this.props.onChange}
          />

           <Select
             name="pack_2_set"
             label="Second Pack Set"
             value={this.props.pod.pack_2_set}
             options={this.props.sets.map(function(set) {return {value: set.code, display: set.name, selected: false}} )}
             onChange={this.props.onChange}
           />

            <Select
              name="pack_3_set"
              label="Third Pack Set"
              value={this.props.pod.pack_3_set}
              options={this.props.sets.map(function(set) {return {value: set.code, display: set.name, selected: false}} )}
              onChange={this.props.onChange}
            />

          {players}

          <input
            type="submit"
            disabled={this.props.saving}
            className="btn btn-primary"
            onClick={this.props.onSave}/>
        </form>
      </div>
  );
  }
}

PodForm.propTypes = {
  pod: React.PropTypes.object.isRequired,
  sets: React.PropTypes.array.isRequired,
  onSave: React.PropTypes.func.isRequired,
  onChange: React.PropTypes.func.isRequired,
  onPlayerChange: React.PropTypes.func.isRequired,
  saving: React.PropTypes.bool
};

export default PodForm;
