import React, {PropTypes} from 'react';

const Select = ({name, label, value, onChange, options}) => {
  return (
    <div className="form-group">
      <label htmlFor={name}>{label}</label>
      <div className="field">
        <select
          name={name}
          className="form-control"
          onChange={onChange}
          value={value}>
          {options.map(option =>
            <option key={option.value} value={option.value}>{option.display}</option>
          )}
        </select>
      </div>
    </div>
  );
};

Select.propTypes = {
  name: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  options: PropTypes.array.isRequired
};

export default Select;
