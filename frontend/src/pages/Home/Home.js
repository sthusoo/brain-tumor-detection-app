  
import './Home.css';
import React, { Component } from 'react';
import { Row, Col, Container, Form, Button } from 'react-bootstrap';
// import axios from 'axios';
// https://www.kaggle.com/navoneel/brain-mri-images-for-brain-tumor-detection

class Home extends Component {
  constructor(props) {
    super(props);
    this.handleUpload = this.handleUpload.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

    this.state = { 
      image: null,
      classification: null,
      prediction: null,
      image_src: null
    };
  }

  handleUpload = (e) => {
    console.log(e.target.value + e.target.name);
    if (e.target.files[0]) {
      const imageFile = e.target.files[0];
      console.log(imageFile)
      this.setState(() => ({image: imageFile}))
    }
  }

  handleSubmit =  async (event) => {
    const image = this.state.image;
    const data = new FormData();
    data.append('file', image);

    await fetch('http://127.0.0.1:5000/', {
        method: 'POST',
        body: data
      }).then((response) => {  return response.json() }).then((data) => 
      {  
        console.log(data)
        this.setState(() => ({classification: data.classification, prediction: data.prediction, image_src: data.imagePath }))
        return data
      })
  }
 
  render() {
    return (
      <div className="App">
          <Container className='title'>
            <h1> Brain Tumor Detection </h1>
          </Container>
          <Container>
            <Row id='upload-body'>
              <Form>
                  <Col>
                      <span>Upload Brain MRI:</span>
                      <Form.Control type="file" name='image' onChange={this.handleUpload} />
                  </Col>
              </Form>
            </Row>
          </Container>
          <Container>
            <Row>
              <Button id='submit-button' onClick={this.handleSubmit}>Submit</Button>
            </Row>
            { this.state.image_src ? 
                <Row id='predict'><img width='150' height='150' src={this.state.image_src} class='img-thumbnail' /></Row>
                : <Row></Row>
            }
            <Row id='predict'>
              <h4>Prediction: </h4>
            </Row>   
            { this.state.classification != null ? 
            <Row id='predict'>
              { (this.state.classification == 'Tumor') ? 
              <p>This MRI is likely that of a Brain Tumor</p> : <p>This MRI is likely that of a Normal Brain</p> 
              }
            </Row> : <Row></Row>
            }
        </Container>
      </div>
    );
  }
}

export default Home;