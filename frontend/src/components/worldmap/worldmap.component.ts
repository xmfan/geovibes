import { Component, OnInit } from '@angular/core';

declare let $: any;
declare let jQuery: any;
declare let THREE: any;
declare let meshClouds: any;
declare let sp: any;

@Component({
  selector: 'worldmap',
  templateUrl: './worldmap.component.html',
  styleUrls: ['./worldmap.component.css']
})
export class WorldmapComponent implements OnInit {

  POS_X = 1800;
  POS_Y = 500;
  POS_Z = 1800;
  WIDTH = 1000;
  HEIGHT = 600;

  FOV = 45;
  NEAR = 1;
  FAR = 4000;

  renderer;
  mapDiv;
  camera;
  scene;
  light;
  sp;
  meshClouds;

  constructor() { }

  ngOnInit() {
    // couple of constants

    this.renderer = new THREE.WebGLRenderer();
    this.renderer.setSize(this.WIDTH,this.HEIGHT);
    this.renderer.setClearColorHex(0x111111);

    this.mapDiv = document.getElementById("globe");
    this.mapDiv.appendChild(this.renderer.domElement);

    this.camera = new THREE.PerspectiveCamera(this.FOV,this.WIDTH/this.HEIGHT,this.NEAR,this.FAR);
    this.camera.position.set(this.POS_X,this.POS_Y, this.POS_Z);
    this.camera.lookAt(new THREE.Vector3(0,0,0));

    this.scene = new THREE.Scene();
    this.scene.add(this.camera);

    // this can get replaced with angular code
    jQuery.get('../../assets/data/density.csv', (data) => {
        this.addDensity(this.CSVToArray(data));
        this.addLights();
        this.addEarth();
        this.addClouds();
        this.render();
    });
  }



    // simple function that converts the density data to the markers on screen
    // the height of each marker is relative to the density.
    private addDensity = (data) => {

        // the geometry that will contain all our cubes
        let geom = new THREE.Geometry();
        // material to use for each of our elements. Could use a set of materials to
        // add colors relative to the density. Not done here.
        let cubeMat = new THREE.MeshLambertMaterial({color: 0x000000,opacity:0.6, emissive:0xffffff});
        for (let i = 0 ; i < data.length-1 ; i++) {

            //get the data, and set the offset, we need to do this since the x,y coordinates
            //from the data aren't in the correct format
            let x = parseInt(data[i][0])+180;
            let y = (parseInt((data[i][1]))-84)*-1;
            let value = parseFloat(data[i][2]);

            // calculate the position where we need to start the cube
            let position = this.latLongToVector3(y, x, 600, 2);

            // create the cube
            let cube = new THREE.Mesh(new THREE.CubeGeometry(5,5,1+value/8,1,1,1,cubeMat));

            // position the cube correctly
            cube.position = position;
            cube.lookAt( new THREE.Vector3(0,0,0) );

            // merge with main model
            THREE.GeometryUtils.merge(geom,cube);
          // scene.add(cube);
        }

        // create a new mesh, containing all the other meshes.
        let total = new THREE.Mesh(geom,new THREE.MeshFaceMaterial());

        // and add the total mesh to the scene
        this.scene.add(total);
    }

    // add a simple light
    private addLights = () => {
        this.light = new THREE.DirectionalLight(0x3333ee, 3.5, 500 );
        this.scene.add( this.light );
        this.light.position.set(this.POS_X,this.POS_Y,this.POS_Z);
    }

    // add the earth
    private addEarth = () => {
        let spGeo = new THREE.SphereGeometry(600,50,50);
        let planetTexture = THREE.ImageUtils.loadTexture( "../../assets/img/world-big-2-grey.jpg" );
        let mat2 =  new THREE.MeshPhongMaterial( {
            map: planetTexture,
            perPixel: false,
            shininess: 0.2 } );
        this.sp = new THREE.Mesh(spGeo,mat2);
        this.scene.add(this.sp);
    }

    // add clouds
    private addClouds = () => {
        let spGeo = new THREE.SphereGeometry(600,50,50);
        let cloudsTexture = THREE.ImageUtils.loadTexture( "../../assets/img/earth_clouds_1024.png" );
        let materialClouds = new THREE.MeshPhongMaterial( { color: 0xffffff, map: cloudsTexture, transparent:true, opacity:0.3 } );

        this.meshClouds = new THREE.Mesh( spGeo, materialClouds );
        this.meshClouds.scale.set( 1.015, 1.015, 1.015 );
        this.scene.add( this.meshClouds );
    }

    // convert the positions from a lat, lon to a position on a sphere.
    private latLongToVector3(lat, lon, radius, heigth) {
        let phi = (lat)*Math.PI/180;
        let theta = (lon-180)*Math.PI/180;

        let x = -(radius+heigth) * Math.cos(phi) * Math.cos(theta);
        let y = (radius+heigth) * Math.sin(phi);
        let z = (radius+heigth) * Math.cos(phi) * Math.sin(theta);

        return new THREE.Vector3(x,y,z);
    }

  // render the scene
  private render = () => {
      let timer = Date.now() * 0.0001;
      this.camera.position.x = (Math.cos( timer ) *  1800);
      this.camera.position.z = (Math.sin( timer ) *  1800) ;
      this.camera.lookAt( this.scene.position );
      this.light.position = this.camera.position;
      this.light.lookAt(this.scene.position);
      this.renderer.render( this.scene, this.camera );
      requestAnimationFrame( this.render );
  }

  // from http://stackoverflow.com/questions/1293147/javascript-code-to-parse-csv-data
    
  private CSVToArray( strData, strDelimiter? ){
      // Check to see if the delimiter is defined. If not,
      // then default to comma.
      strDelimiter = (strDelimiter || ",");

      // Create a regular expression to parse the CSV values.
      let objPattern = new RegExp(
              (
                  // Delimiters.
                      "(\\" + strDelimiter + "|\\r?\\n|\\r|^)" +

                          // Quoted fields.
                              "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +

                          // Standard fields.
                              "([^\"\\" + strDelimiter + "\\r\\n]*))"
                      ),
              "gi"
      );


      // Create an array to hold our data. Give the array
      // a default empty first row.
      let arrData = [[]];

      // Create an array to hold our individual pattern
      // matching groups.
      let arrMatches = null;


      // Keep looping over the regular expression matches
      // until we can no longer find a match.
      while (arrMatches = objPattern.exec( strData )){

          // Get the delimiter that was found.
          let strMatchedDelimiter = arrMatches[ 1 ];

          // Check to see if the given delimiter has a length
          // (is not the start of string) and if it matches
          // field delimiter. If id does not, then we know
          // that this delimiter is a row delimiter.
          if (
                  strMatchedDelimiter.length &&
                          (strMatchedDelimiter != strDelimiter)
                  ){

              // Since we have reached a new row of data,
              // add an empty row to our data array.
              arrData.push( [] );

          }


          // Now that we have our delimiter out of the way,
          // let's check to see which kind of value we
          // captured (quoted or unquoted).
          let strMatchedValue = ''; 
          
          if (arrMatches[ 2 ]){

              // We found a quoted value. When we capture
              // this value, unescape any double quotes.
              let strMatchedValue = arrMatches[ 2 ].replace(
                      new RegExp( "\"\"", "g" ),
                      "\""
              );

          } else {

              // We found a non-quoted value.
              strMatchedValue = arrMatches[ 3 ];

          }


          // Now that we have our value string, let's add
          // it to the data array.
          arrData[ arrData.length - 1 ].push( strMatchedValue );
      }

      // Return the parsed data.
      return( arrData );
  }

}
