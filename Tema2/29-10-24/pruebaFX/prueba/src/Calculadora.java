import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

public class Calculadora extends Application {
    @Override
    public void start(Stage stage) {
        Label label1 = new Label("numero1:");
        Label label2 = new Label("numero2:");
        TextField numero1_text = new TextField();
        TextField numero2_text = new TextField();
        Label lbl_resultado = new Label("Resultado:");
        TextField resultado = new TextField();
        Button sumar = new Button("sumar");

        GridPane grid = new GridPane();
        grid.add(label1, 0, 0);
        grid.add(numero1_text, 1, 0);
        grid.add(label2, 0, 1);
        grid.add(numero2_text, 1, 1);
        grid.add(lbl_resultado, 0, 2);
        grid.add(resultado, 1, 2);
        grid.add(sumar, 1, 3);

        Scene scene = new Scene(grid, 300, 200);
        stage.setScene(scene);
        stage.setTitle("Calculadora");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
