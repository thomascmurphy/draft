import React, {PropTypes} from 'react';

const Select = ({name, label, onChange, options}) => {
  return (
    <div className="form-group">
      <label htmlFor={name}>{label}</label>
      <div className="field">
        <select
          name={name}
          className="form-control"
          onChange={onChange}>
          {this.props.options.map(option =>
            <option key={option.value} value={option.value} selected={option.selected}>{option.display}</option>
          )}
        </select>
      </div>
    </div>
  );
};

Select.propTypes = {
  name: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  options: PropTypes.array.isRequired
};

export default Select;
