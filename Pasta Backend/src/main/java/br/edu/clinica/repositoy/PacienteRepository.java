package br.edu.clinica.repository;

import br.edu.clinica.model.Paciente;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PacienteRepository extends JpaRepository<Paciente, Long> {
    boolean existsByCpf(String cpf);
    boolean existsByEmail(String email);
}
