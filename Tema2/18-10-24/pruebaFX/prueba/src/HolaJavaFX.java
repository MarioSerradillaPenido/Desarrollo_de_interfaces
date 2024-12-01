import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.stage.Stage;

public class HolaJavaFX extends Application {

    @Override
    public void start(Stage stage) {
        // Crear un label con el texto
        Label mensaje = new Label("Hola, JavaFX");
        
        // Crear la escena con el Label
        Scene scene = new Scene(mensaje, 300, 200);
        
        // Configurar el stage (ventana)
        stage.setTitle("Mi primera aplicación JavaFX");
        stage.setScene(scene);
        stage.show(); // Mostrar la ventana
    }

    public static void main(String[] args) {
        launch(args); // Iniciar la aplicación
    }
}