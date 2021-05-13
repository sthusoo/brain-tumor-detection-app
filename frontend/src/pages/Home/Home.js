  
import './Home.css';
import React, { Component } from 'react';
import { Row, Col, Container, Form, Button } from 'react-bootstrap';
import Particles from 'react-particles-js';
import { storage } from '../../components/Firebase/firebase';

class Home extends Component {
  constructor(props) {
    super(props);
    this.handleUpload = this.handleUpload.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

    this.state = { 
      image: null,
      classification: null,
      prediction: null,
      image_src: null,
      progress: null,
      confidence_percent: null,
      uploaded: false
    };
  }

//   componentDidMount() {
//     this.interval = setInterval(() => { 
//       this.predict()
//     }, 200);
//     this.predict(); // also load one immediately
// }
// componentWillUnmount(){
//   clearInterval(this.state.interval)
// }

  handleUpload = (e) => {
    if (e.target.files[0]) {
      const imageFile = e.target.files[0];
      this.setState(() => ({image: imageFile, uploaded: false}))
    }
  }

  handleSubmit = async () => {
    const image = this.state.image;
    const uploadTask = storage.ref(`images/${image.name}`).put(image);
    uploadTask.on(
      "state_changed",
      snapshot => {
        const progress = Math.round(
          (snapshot.bytesTransferred / snapshot.totalBytes) * 100
        );
        this.setState(() => ({progress: progress}))
      },
      error => {
        console.log(error);
      },
      () => {
        storage
          .ref("images")
          .child(image.name)
          .getDownloadURL()
          .then(url => {
            this.setState(() => ({image_src: url, uploaded: true}))
          });
      }
    );
    this.callback()
  }

  callback = () => {
    if (this.state.uploaded) {
      this.predict();
    }
  }

  // interval = (callback) => {
  //   let uploaded = this.state.uploaded
  //   const checkUploadStatus = setInterval(function() {
  //     if (uploaded == true) {
  //       callback()
  //       clearInterval(checkUploadStatus)
  //     }
  //   }, 200);
  // }

  predict = async () => {
    const image = this.state.image;
    const data = new FormData();
    data.append('file', image);

    const image_src = this.state.image_src; 
    
    await fetch('http://127.0.0.1:5000/', {
        method: 'POST',
        body: image_src
      }).then((response) => {  return response.json() }).then((data) => 
      {  
        console.log(data)
        this.setState(() => ({classification: data.classification, prediction: data.prediction, confidence_percent: data.confidence }))
        return data
      })
  }
 
  render() {
    return (
    <div className="App">
      <div id="particles-js">
      <Particles id="particles-js"
          params={{
            "particles": {
                "number": {
                    "value": 250,
                    "density": {
                        "enable": true,
                        "value_area": 1500
                    }
                },
                "line_linked": {
                    "enable": true,
                    "opacity": 0.1
                },
                "move": {
                    "speed": 0.2
                },
                "size": {
                    "value": 1
                },
                "opacity": {
                    "anim": {
                        "enable": true,
                        "speed": 1,
                        "opacity_min": 2
                    }
                }
            },
            "interactivity": {
                "events": {
                    "onclick": {
                        "enable": true,
                        "mode": "push"
                    }
                },
                "modes": {
                    "push": {
                        "particles_nb": 2
                    }
                }
            },
            "retina_detect": true
        }} />
        </div>
          <Container className='title'>
            <h1> Brain Tumor Detection </h1>
          </Container>
          <Container>
            <Row id='center'>
              Please upload an Brain MRI below.
            </Row>
            <Row id='upload-body'>
              <Form>
                  <Col>
                      <Form.Control type="file" name='image' onChange={this.handleUpload} />
                  </Col>
              </Form>
            </Row>
          </Container>
          <Container>
          <Row>
              <Button id='submit-button' onClick={this.handleSubmit}>Submit</Button>
          </Row>
            {/* { this.state.uploaded ? 
             <Row>
             <Button id='submit-button' onClick={this.predict}>Submit</Button>
            </Row> : <Row></Row>
            } */}
            { this.state.image_src != null ? 
                <Row id='predict'><img width='150' height='150' src={this.state.image_src} className='img-thumbnail' /></Row>
                : <Row></Row>
            } 
            { this.state.classification != null ?
            <Row id='predict'>
              <h4>Prediction</h4>
            </Row> : <Row></Row>
            }
            { this.state.classification != null && this.state.uploaded ? 
            <Row id='predict'>
              { (this.state.classification == 'Tumor') ? 
              <p>The MRI is most likely that of a Brain Tumor with a confidence of { this.state.confidence_percent }%</p> : <p>This MRI is most likely that of a Normal Brain with a confidence of { this.state.confidence_percent }%</p> 
              }
            </Row> : <Row></Row>
            }
        </Container>
      
    </div>
    );
  }
}

export default Home;