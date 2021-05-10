  
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
      image: null
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
      }).then((response) => {  return response.json() }).then((data) => console.log(data))
  }
 
  render() {


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
                                <Form.Control type="file" name='image' onChange={this.handleUpload} />
                            </Col>
                        </Row>
                        <Row>
                            <Button id='submit-button' content="Submit" onClick={this.handleSubmit} />
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