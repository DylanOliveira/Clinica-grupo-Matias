package controller;


import br.edu.clinica.dto.LoginRequest;
import br.edu.clinica.model.Usuario;
import br.edu.clinica.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/auth")
public class AuthController {

    @Autowired
    private UsuarioRepository usuarioRepo;

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest req) {

        Usuario u = usuarioRepo.findByEmail(req.getEmail()).orElse(null);
        if (u == null) return ResponseEntity.status(401).body("Usuário não encontrado");
        if (!u.getSenha().equals(req.getSenha())) return ResponseEntity.status(401).body("Senha incorreta");
       
        return ResponseEntity.ok("Login OK - token será gerado depois");
    }
}

