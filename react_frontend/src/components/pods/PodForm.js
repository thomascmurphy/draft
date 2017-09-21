import React, {PropTypes} from 'react';
import TextInput from '../common/TextInput';
import Select from '../common/Select';

class PodForm extends React.Component {
  constructor(props) {
    super(props);
    this.makeCheckBoxes = this.makeCheckBoxes.bind(this);
  }

  makePlayerBoxes() {
    return this.props.players.map(player => {
      return (
        <TextInput
          item={player.id}
          handleChange={this.props.onPlayerChange}
          key={player.id}/>
      );
    });
  }

  render() {
    const players = this.makePlayerBoxes();
    return (
      <div>
        <form>
          <TextInput
            name="name"
            label="name"
            value={this.props.pod.name}
            onChange={this.props.onChange}/>

          <Select
            name="pack_1_set"
            label="First Pack Set"
            options={this.props.sets.map((set) => {value: set.code, display: set.name, selected: false})}
          />

           <Select
             name="pack_2_set"
             label="Second Pack Set"
             options={this.props.sets.map((set) => {value: set.code, display: set.name, selected: false})}
           />

            <Select
              name="pack_3_set"
              label="Third Pack Set"
              options={this.props.sets.map((set) => {value: set.code, display: set.name, selected: false})}
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
  players: React.PropTypes.array.isRequired,
  sets: React.PropTypes.array.isRequired,
  onSave: React.PropTypes.func.isRequired,
  onChange: React.PropTypes.func.isRequired,
  onPlayerChange: React.PropTypes.func.isRequired,
  saving: React.PropTypes.bool
};

export default PodForm;
