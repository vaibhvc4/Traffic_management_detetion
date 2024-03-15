
import React, { useState } from 'react';
import axios from 'axios';

function InputForm() {
  const [vehicleNumber, setVehicleNumber] = useState('');
  const [responseJson, setResponseJson] = useState(null);

  const handleInputChange = (event) => {
    setVehicleNumber(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post('http://localhost:8000/vehicle_number', { vehicle_no: vehicleNumber });
      setResponseJson(response.data);
      console.log('Submitted Vehicle Number:', vehicleNumber);
    } catch (error) {
      console.error('Error submitting Vehicle Number:', error);
    }
  };

  return (
    <div style={{ backgroundColor: 'grey' }} className='table'>
      <h2>Vehicle Number Form</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Vehicle Number:
          <input
            type="text"
            value={vehicleNumber}
            onChange={handleInputChange}
          />
        </label>
        <button type="submit">Submit</button>
      </form>

      {responseJson && (
        <div>
          <h2>VIOLATION DETAILS</h2>
          <table style={{ backgroundColor: 'black' }} className="table" >
            <thead>
              <tr>
              <th style={{ padding: '8px' }}>Notice ID</th>
                <th style={{ padding: '8px' }}>Vehicle Number</th>
                <th style={{ padding: '8px' }}>Helmet Status</th>
                <th style={{ padding: '8px' }}>Insurance Status</th>
                <th style={{ padding: '8px' }}>Emission Status</th>
                <th style={{ padding: '8px' }}>Violation ID</th>
              </tr>
              
            </thead>
            <tbody>
              
              {responseJson.violation.map((item, index) => (
                <tr key={index}>
                  <td>{item[0]}</td>
                  <td>{item[1]}</td>
                  <td>{item[2]}</td>
                  <td>{item[3]}</td>
                  <td>{item[4]}</td>
                  <td>{item[5]}</td>
                </tr>
              ))}
            </tbody>
            <thead>
              <tr>
              <th style={{ padding: '8px' }}>Payment ID</th>
                <th style={{ padding: '8px' }}>Notice ID</th>
                <th style={{ padding: '8px' }}>Vehicle Number</th>
                <th style={{ padding: '8px' }}>Helmet Fine</th>
                <th style={{ padding: '8px' }}>Insurance Fine</th>
                <th style={{ padding: '8px' }}>Emission Fine</th>
                <th style={{ padding: '8px' }}>Total Fine</th>
                <th style={{ padding: '8px' }}>Payment Date</th>
                </tr>
              
            </thead>

            <tbody>
              
              {responseJson.payments.map((item, index) => (
                <tr key={index}>
                  <td>{item[0]}</td>
                  <td>{item[1]}</td>
                  <td>{item[2]}</td>
                  <td>{item[3]}</td>
                  <td>{item[4]}</td>
                  <td>{item[5]}</td>
                  <td>{item[6]}</td>
                  <td>{item[7]}</td>
                  <td>{item[8]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default InputForm;