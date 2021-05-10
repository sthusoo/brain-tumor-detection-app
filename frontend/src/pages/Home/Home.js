  
import './Home.css';
import React, { Component } from 'react';
import { Row, Col, Container, Form } from 'react-bootstrap';
// import axios from 'axios';
// https://www.kaggle.com/navoneel/brain-mri-images-for-brain-tumor-detection
class Home extends Component {
  constructor(props) {
    super(props);
    // this.handleUpload = this.handleUpload.bind(this);

    this.state = { };
  }
 
  render() {
    async function classifyImage() {
      // let resp = null;
      // const apiUrl = ``;
      // return axios.get(apiUrl).then(response => {
      //     resp = response.data
      //     return resp
      // })
      await fetch('http://127.0.0.1:5000/predict_api', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      }).then((response) => {  return response.json() }).then((data) => console.log(data))
  }

  function handleUpload() {
        // Call Predict API
    classifyImage()
  }

    return (
      <div className="App">
          <Container className='title'>
            <h1> Brain Tumor Detection </h1>
          </Container>
          <Container>
            <Row>
                <Col>
                    <Form>
                        <Row id='upload-body'>
                            <Col id='upload'>
                                <span> Upload Brain MRI:</span>
                                <input id='actual-btn' type="file" name="file" onChange={handleUpload} hidden/>
                                <label for="actual-btn">Choose File</label>
                                <span id="file-chosen">No file chosen</span>
                            </Col>
                        </Row>
                        <Row>
                            <input id='submit-button' type="submit" value="Submit" />
                        </Row>
                    </Form>
                </Col>
                <Col>
                    {/* <img width='150' height='150' src={ image_src } class='img-thumbnail' /> */}
                    <h4>Prediction: </h4>
                </Col>
            </Row>
          </Container>
      </div>
    );
  }
}

export default Home;