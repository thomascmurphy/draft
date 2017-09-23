import React, {PropTypes} from 'react';
import TextInput from '../common/TextInput';

class EmailForm extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <form>
          <TextInput
            name="email"
            label="Your Email"
            value={this.props.email}
            onChange={this.props.onChange}/>

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

EmailForm.propTypes = {
  onChange: React.PropTypes.func.isRequired,
  onSave: React.PropTypes.func.isRequired,
  saving: React.PropTypes.bool,
  email: React.PropTypes.string
};

export default EmailForm;