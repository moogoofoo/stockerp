import dash_html_components as html
import dash_echarts
from datetime import datetime
import dash, sys




def main():
    '''
    dash_echarts examples
    name: air with echarts
    author: dameng <pingf0@gmail.com>
    '''
    external_scripts = [
        f'https://webapi.amap.com/maps?v=1.4.15&key={sys.argv[1]}&plugin=Map3D',
        "https://a.amap.com/jsapi_demos/static/demo-center/model/js/three.js",
        "https://a.amap.com/jsapi_demos/static/demo-center/model/js/loaders/MTLLoader.js",
        "https://a.amap.com/jsapi_demos/static/demo-center/model/js/loaders/LoaderSupport.js",
        "https://a.amap.com/jsapi_demos/static/demo-center/model/js/loaders/OBJLoader2.js"
    ]
    app = dash.Dash(__name__,
        external_scripts=external_scripts
    )
    data = [
        [113.625328, 34.746611, 12600574],  # 郑州
        [121.4737021, 31.2303904, 24870895],  # 上海
        [116.3474879, 39.9432725, 21893095],  # 北京
    ]

    def convert(e):
        e[2] /= 100000
        return e

    def get_data():
        return [convert(e) for e in data]

    option = {
          'amap': {
            'viewMode': '3D',
            'center': [116.472605, 39.992075],
            'resizeEnable': True,
            'mapStyle': 'amap://styles/light',
            'renderOnMoving': True,
            'echartsLayerInteractive': True,
            'largeMode': True,
            'zoom': 17,
            'pitch': 55,
            'showBuildingBlock': True,
          },
          'series': [
            {
                'type': 'scatter',
                'coordinateSystem': 'amap',
                'symbolSize': 'div10',
                'data': get_data(),
                'encode': {
                  # encode the third element of data item as the `value` dimension
                  'value': 2
                }
            },
        ]
          # 'series': [
          #   {
          #     'type': 'scatter3D',
          #     'coordinateSystem': 'amap',
          #     'data': [[120, 30, 8], [120.1, 30.2, 20]],
          #     'encode': {
          #       # encode the third element of data item as the `value` dimension
          #       'value': 2
          #     }
          #   }
          # ]
        }

    app.layout = html.Div([
        dash_echarts.DashECharts(
            option = option,
            id='echarts',

            fun_values= ["div10", "init"],
            fun_loaded= ["init"],
            funs= {
                'div10': '''
                function(val) {
                    return val[2] / 10;
                }
                ''',
                'init': '''
function init() {
    console.log('---------->1', this.chart);
    console.log('---------->2', this.amap);
    console.log(this.chart.getModel());
    var amapComponent = this.chart.getModel().getComponent('amap');
    // Get the instance of AMap
    var map = amapComponent.getAMap();
    
    
    map.AmbientLight = new AMap.Lights.AmbientLight([1,1,1],1);
            map.DirectionLight = new AMap.Lights.DirectionLight([1,0,-0.5],[1,1,1],1);

            var loadModel = function () {
                var modelName = 'building';
                var scope = this;
                var objLoader = new THREE.OBJLoader2();
                var callbackOnLoad = function ( event ) {
                    var object3Dlayer = new AMap.Object3DLayer();
                    var meshes = event.detail.loaderRootNode.children;
                    for(var i=0;i<meshes.length;i++){
                        var vecticesF3 = meshes[i].geometry.attributes.position;
                        var vecticesNormal3 = meshes[i].geometry.attributes.normal;
                        var vecticesUV2 = meshes[i].geometry.attributes.uv;
                        
                        var vectexCount =  vecticesF3.count;

                        mesh = new AMap.Object3D.MeshAcceptLights();

                        var geometry = mesh.geometry;
                    
                        //底部一圈
                        // debugger

                        var c,opacity;

                        var material = meshes[i].material[0]||meshes[i].material;
                        // debugger
                        if(material.map)
                        mesh.textures.push('https://a.amap.com/jsapi_demos/static/demo-center/model/1519/1519.bmp')
                        
                        c = material.color;
                        opacity = material.opacity
                        
                        // debugger
                        for(var j=0;j<vectexCount;j+=1){
                            var s = j*3;
                            geometry.vertices.push(vecticesF3.array[s],vecticesF3.array[s+2],-vecticesF3.array[s+1]);
                        
                            if(vecticesNormal3) {
                                geometry.vertexNormals.push(vecticesNormal3.array[s],vecticesNormal3.array[s+2],-vecticesNormal3.array[s+1]);
                            }
                            if(vecticesUV2) {
                                geometry.vertexUVs.push(vecticesUV2.array[j*2],1-vecticesUV2.array[j*2+1]);
                            }
                            geometry.vertexColors.push(c.r,c.g,c.b,opacity)
                        }
                        // debugger
                        mesh.DEPTH_TEST = material.depthTest
                        // mesh.backOrFront = 'both'
                        mesh.transparent = opacity<1;
                        mesh.scale(6,6,6)
                        mesh.rotateZ(-48)
                        mesh.position(new AMap.LngLat(116.472605,39.992075))
                        object3Dlayer.add(mesh)
                    }
                    map.add(object3Dlayer)
                };

                var onLoadMtl = function ( materials ) {
                    // for(var i=0;i<materials.length;i+=1){
                    // 	materials[i].side=2;
                    // }
                    objLoader.setModelName( modelName );
                    objLoader.setMaterials( materials );
                    objLoader.load( 'https://a.amap.com/jsapi_demos/static/demo-center/model/1519/1519.obj', callbackOnLoad, null, null, null, false );
                };
                objLoader.loadMtl( 'https://a.amap.com/jsapi_demos/static/demo-center/model/1519/1519.mtl', null, onLoadMtl );
            };
            var A  = new AMap.Text({
                text:'XX大厦A座',
                position:[116.472476,39.991878],
                height:650,
                verticalAlign:'bottom',
                map:map,
                style:{
                    'background-color':'red',
                    'border-color':'white',
                    'font-size':'12px'
                }
            })
            
            var B  = new AMap.Text({
                text:'XX大厦B座',
                verticalAlign:'bottom',
                position:[116.47286,39.992178],
                height:651,
                map:map,
                style:{
                    'background-color':'red',
                    'border-color':'white',
                    'font-size':'12px'
                }
            })
            new AMap.Circle({
                center:[116.47246,39.992133],
                map:map,
                radius:700,
                fillColor:'blue',
                strokeWeight:1,
                strokeColor:'white',
                fillOpacity:0.05
            })
            new AMap.Circle({
                center:[116.47246,39.992133],
                map:map,
                radius:500,
                fillColor:'blue',
                strokeWeight:1,
                strokeColor:'white',
                fillOpacity:0.05
            })
            new AMap.Circle({
                center:[116.47246,39.992133],
                map:map,
                radius:300,
                fillColor:'blue',
                strokeWeight:1,
                strokeColor:'white',
                fillOpacity:0.05
            })
            var shopping = new AMap.Marker({
                icon:'https://a.amap.com/jsapi_demos/static/resource/shopping.png',
                offset:new AMap.Pixel(-32,-54),
                position:[116.468833,39.992834],
                map:map,
            })
            new AMap.Polyline({
                path:[[116.47246,39.992133],[116.468833,39.992834]],
                strokeColor:'blue',
                lineCap:'round',
                isOutline:true,
                outlineColor:'white',
                showDir:true,
                map:map,
                strokeWeight:5,
                borderWeight:2,
                strokeOpacity:0.5
            })
            new AMap.Text({
                text:'购物320米',
                position:[116.470123,39.992572],
                map:map,
                style:{
                    'background-color':'#ccccff',
                    'border-color':'white',
                    'font-size':'12px'
                }
            })
            var hospital = new AMap.Marker({
                icon:'https://a.amap.com/jsapi_demos/static/resource/hospital.png',
                offset:new AMap.Pixel(-32,-54),
                position:[116.473154,39.997106],
                map:map,
            })
            new AMap.Polyline({
                path:[[116.47246,39.992133],[116.473154,39.997106]],
                strokeColor:'red',
                lineCap:'round',
                isOutline:true,
                outlineColor:'white',
                showDir:true,
                map:map,
                strokeWeight:5,
                borderWeight:2,
                strokeOpacity:0.5
            })
            new AMap.Text({
                text:'医院550米',
                position:[116.472836,39.994887],
                map:map,
                style:{
                    'background-color':'#ccccff',
                    'border-color':'white',
                    'font-size':'12px'
                }
            })
            var school = new AMap.Marker({
                icon:'https://a.amap.com/jsapi_demos/static/resource/school.png',
                offset:new AMap.Pixel(-32,-54),
                position:[116.47106,39.994558],
                map:map
            })
            new AMap.Polyline({
                path:[[116.47246,39.992133],[116.47106,39.994558]],
                strokeColor:'green',
                lineCap:'round',
                isOutline:true,
                outlineColor:'white',
                showDir:true,
                map:map,
                strokeWeight:5,
                borderWeight:2,
                strokeOpacity:0.5
            })
            new AMap.Text({
                text:'学校300米',
                position:[116.471626,39.993571],
                map:map,
                style:{
                    'background-color':'#ccccff',
                    'border-color':'white',
                    'font-size':'12px'
                }
            })
            loadModel()
    
    
    
		
}
                ''',
            },
            style={
                "width": '100vw',
                "height": '100vh',
            }
        ),
    ])
    app.run_server(debug=True)

if __name__ == '__main__':
    main()
