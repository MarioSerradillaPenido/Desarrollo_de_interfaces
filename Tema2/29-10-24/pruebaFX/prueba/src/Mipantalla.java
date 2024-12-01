import javafx.application.Application;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import javafx.stage.stage;

public class MiPantalla extends Application{

    @Override
    public void start (Stage stage) {
        //aqui comienza logicamente la pantalla
        Label label = new Label ("Ingrese su nombre:");

        //untexto
        TextField campoTexto = new TextField();

        //botonº
        Button boton = new Button("Aceptar");
        Tooltip tooltip = new Tooltip("mensaje");
        boton.setTooltip(tooltip);

        DropShadow sombra = new DropShadow();
        boton.setEffect(sombra);

        boton.setOnMouseEntered(e -> boton.setStyle("-fx-background-color:#ff0000;"));
        boton.setOnMouseEntered(e -> boton.setStyle("-fx-background-color:#ffffff;"));

        boton.setOnAction(e -> {
            String nombre = campoTexto.getText();
            System.out.println(nombre);
        })
        VBox layout = new Vbox(10);
        layout.getChildren().addAll(label, campoTexto, boton);

        Scene escena = new Scene(layout,300,200);
        stage.setScene(escena);
        stage.setTitle("mi pantalla que bonica");
        stage.show();
    }

    public static void main (String[] args){
        launch(args);
    }
}